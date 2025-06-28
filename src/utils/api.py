from aiohttp import ClientError, ClientSession
from asyncio import sleep
from dotenv import load_dotenv
from io import BytesIO
from json import dumps, loads
from os import getenv
from telethon import Button, events, TelegramClient
from telethon.errors import ForbiddenError, MessageNotModifiedError
from typing import List, Literal
from websockets import connect

from utils.error import APIError, IgnoreError
from utils.general import get_entity, get_username
from utils.typess import APICommandResponse, APITelegramWSPayloadChats, APITelegramWSPayloadSend, APITelegramWSResponse, CommandResponse
from utils.update_chatcount import get_bot_dialog_ids

from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.messages import DeleteChatRequest, DeleteChatUserRequest
from telethon.tl.types import Channel, Chat, ChatForbidden

load_dotenv()
API_URL: str = getenv('API_URL', 'https://api.pokehunt.xyz')
API_KEY: str = getenv('API_KEY', '')
API_WS_KEY: str = getenv('API_WS_KEY', '')

if not API_KEY:
    raise ValueError('No pokehunt API key specified!')

if not API_WS_KEY:
    raise ValueError('No pokehunt API WS key specified!')

ws = None
wsQueue = []

async def create_ws_connection(client: TelegramClient):
    global ws
    global wsQueue

    while True: # Infinite loop to avoid recursion
        try:
            ws = await connect(
                f"{API_URL.replace('http', 'ws')}/client",
                subprotocols=["Authorization", "telegram", API_WS_KEY],
            )  # https -> wss, http -> ws
            print("Connected to the Pokéhunt API")

            for msg in wsQueue:
                await ws.send(msg)
            wsQueue = []

            async for message in ws:
                try:
                    json: APITelegramWSResponse = loads(message)
                    chat = await get_entity(client, int(json['chatID'])) # chatID is given as string
                    if chat is None:
                        raise Exception('Chat is None (not found)')

                    # TODO: these are always False for some reason
                    # there is also await client.get_permissions(chat.id, await client.get_me()) but these don't include messages/media/photos
                    # permissions = await client.get_permissions(chat)
                    # print(permissions.send_messages)
                    # print(permissions.send_media)
                    # print(permissions.send_photos)

                    toSent = await parse_command_response(client, json)
                    await client.send_message(
                        chat,
                        toSent['content'],
                        file=toSent['files'][0] if toSent['files'] else None,
                        buttons=toSent['buttons'] if toSent['buttons'] else None,
                    )
                except Exception as e:
                    handle_exception(e, None, client, 'api.py')
        except Exception as e:
            ws = None
            print('Disconnected from the Pokéhunt API, retrying in 5 secs')
            await sleep(5)

async def user_sent_message(user_id: int, user_name: str, chat_id: int):
    global ws
    global wsQueue

    to_send: APITelegramWSPayloadSend = {
        'platform': "telegram",
        'event': "send",
        'userID': str(user_id),
        'userName': user_name,
        'chatID': str(chat_id),
    }

    if not ws:
        wsQueue.append(dumps(to_send))
    else:
        await ws.send(dumps(to_send))

async def chat_change(client, event: Literal['added'] | Literal['removed'], id: int, name: str):
    global ws
    global wsQueue

    group_count = 0

    chats = await get_bot_dialog_ids(client)
    for groupID in [c for c in chats if c < 0]:
        try:
            group = await client.get_entity(groupID)
            if isinstance(group, ChatForbidden):
                continue  # If bot is removed from Chat (small group)

            # if isinstance(group, Channel):
            #     await client(LeaveChannelRequest(
            #         channel=group
            #     ))
            #     await client.delete_dialog(group)
            # elif isinstance(group, Chat):
            #     await client(DeleteChatUserRequest(
            #         chat_id=group.id,
            #         user_id='me'
            #     ))
            #     await client.delete_dialog(group)

            if not group.left and (not isinstance(group, Chat) or not group.deactivated):
                group_count += 1
        except:
            # If bot is removed from Channel (mega group) or Channel is deleted, the client.get_entity throws an error
            pass

    to_send: APITelegramWSPayloadChats = {
        'platform': 'telegram',
        'event': event,
        'id': str(id),
        'name': name,
        'total': group_count
    }

    if not ws:
        wsQueue.append(dumps(to_send))
    else:
        await ws.send(dumps(to_send))

async def run_command(client: TelegramClient, event: events.NewMessage, now: int, command: str, args: list) -> CommandResponse:
    user = await event.get_sender()

    url = f"{API_URL}/client/command/{command}"
    headers = {"Authorization": f"{API_KEY}", "Content-Type": "application/json"}
    data = {
        'platform': 'telegram',
        'userID': str(user.id),
        'userName': get_username(user),
        'chatID': str(event.chat_id),
        'timestamp': int(now * 1000),
        'args': args,
    }

    try:
        async with ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as res:
                return await handle_command_response(client, res)
    except ClientError as e:
        print(e)
        raise APIError("The Pokéhunt API is offline")


async def run_callback_command(event, client: TelegramClient, now: int) -> CommandResponse:
    user = await event.get_sender()

    url = f"{API_URL}/client/callbackCommand/{event.data.decode('utf-8')}"
    headers = {"Authorization": f"{API_KEY}", "Content-Type": "application/json"}
    payload = {
        'platform': 'telegram',
		'buttonID': event.data.decode('utf-8'),
		'userID': str(user.id),
		'userName': get_username(user),
		'chatID': str(event.chat_id),
		'timestamp': int(now * 1000),
	}

    try:
        async with ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as res:
                return await handle_command_response(client, res)
    except ClientError:
        raise APIError("The Pokéhunt API is offline")

async def handle_command_response(client: TelegramClient, res) -> CommandResponse:
    if res.status == 400:
        # Malformed request
        raise APIError('An invalid API request was made')
    elif res.status == 401:
        # Invalid API key
        raise APIError("An invalid API key is provided")
    elif res.status == 418:
		# Wrong user pressed button/menu, or callback is wrong/invalid
        raise IgnoreError()
    elif res.status != 200:
        # Other error codes than success
        raise APIError(f"The API server is not responding correctly ({res.status})")

    json: APICommandResponse = await res.json()
    return await parse_command_response(client, json)

async def parse_command_response(client: TelegramClient, json: APICommandResponse | APITelegramWSResponse) -> CommandResponse:
    content = ""
    files = []
    buttons = []

    if 'content' in json:
        content += f"{json['content']}\n"

    for embed in json['embeds']:
        has_content = False
        # if embed.header:
            # content += f"**{embed['header']}**\n"

        if 'title' in embed:
            if embed['title'] != '❌ Error!':
                content += f"**{embed['title']}**\n"
                has_content = True

        if 'description' in embed:
            content += f"{embed['description']}\n"
            has_content = True

        if 'fields' in embed:
            for field in embed['fields']:
                content += f"**{field['name']}**\n{field['value']}\n\n"
                has_content = True

        if 'footer' in embed:
            if embed['footer']: # Make sure it is not {}
                content += f"__{embed['footer']['text']}__\n"
                has_content = True

        if has_content:
            content += "\n"

    for file in json['files']:
        if (
            file['name'] == "oak.jpeg"
            or file['name'] == "start.png"
            or file['name'] == "balance.png"
        ):
            continue
        if len(file['content']['data']) == 0:
            continue

        uploaded_file = await client.upload_file(
            BytesIO(bytes(file['content']['data'])),
            file_name=file['name']
        )
        files.append(uploaded_file)

    for buttonRow in json['buttons']:
        row = []
        for button in buttonRow:
            if 'disabled' in button:
                if button['disabled']:
                    continue

            if button['style'] == "Link":
                row.append(Button.url(button['label'], button['id']))
            else:
                row.append(Button.inline(button['label'], button['id']))
        buttons.append(row)

    # Ignore menu's since Telegram does not support that

    if content == '':
        if len(buttons) > 0:
            content = 'Press any of the buttons below'
        else:
            content = 'This message has no content'

    return { 'content': content, 'files': files, 'buttons': buttons, 'menus': [] }

async def handle_exception(e, event, client, where):
    msg = str(e)

    if isinstance(APIError, e):
        if event is not None:
            cmdRes = await parse_command_response(client, { 'embeds': [{ 'title': '❌ Error!', 'color': '#FF0000', 'description':  str(e) + '. Please contact support here: https://t.me/pokehunt_xyz'}], 'files': [], 'buttons': [], 'menus': [] })
            await event.reply(cmdRes['content'])
    elif isinstance(IgnoreError, e) or isinstance(MessageNotModifiedError, e):
        return
    elif isinstance(ForbiddenError, e):
        if 'You can\'t write in this chat' in msg or 'CHAT_SEND_PLAIN_FORBIDDEN' in msg:
            return # Bot does not have permission to send a message in chat
        elif 'CHAT_SEND_PHOTOS_FORBIDDEN' in msg:
            if event is not None:
                await event.reply('I do not have permissions to send images (of Pokémon) in here. Please make sure to give this to me!')
        else:
            print('.....')
            print(f'An unknown ForbiddenError happened in {where}')
            print(f'Exception Type: {type(e)}')
            print(f'Exception Message: {msg}')
            print('.....')
            if event is not None:
                await event.reply('Please make sure I have enough permissions to send messages and images (of Pokémon) in here!')
    else:
        print('---')
        print(f'An unknown error happened in {where}')
        print(f'Exception Type: {type(e)}')
        print(f'Exception Message: {msg}')
        print('---')
        if event is not None:
            cmdRes = await parse_command_response(client, { 'embeds': [{ 'title': '❌ Error!', 'color': '#FF0000', 'description': 'An unkown error occurred (client). Please contact support here: https://t.me/pokehunt_xyz'}], 'files': [], 'buttons': [], 'menus': [] })
            await event.reply(cmdRes['content'])