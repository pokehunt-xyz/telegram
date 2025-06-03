from asyncio import create_task
from dotenv import load_dotenv
from importlib import import_module
from os import getenv, listdir
from os.path import abspath, dirname, join
from telethon import TelegramClient, events
from telethon.errors.rpcbaseerrors import ForbiddenError
from time import time

from utils.api import chat_change, create_ws_connection, parse_command_response
from utils.error import APIError, IgnoreError
from utils.general import get_username, ignore_bot
from utils.typess import APICommandResponse, APIEmbed, CommandResponse

load_dotenv()

api_id = getenv('TELEGRAM_API_ID')
api_hash = getenv('TELEGRAM_API_HASH')
bot_token = getenv('TELEGRAM_BOT_TOKEN')

if not api_id or not api_hash or not bot_token:
    raise ValueError(
        'API ID, API Hash, or Bot Token is missing. Please check your .env file.'
    )

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def load_commands():
    command_files = [
        f
        for f in listdir(join(dirname(abspath(__file__)), 'commands'))
        if f.endswith('.py') and f != '__init__.py'
    ]

    for command_file in command_files:
        # Dynamically load the command module
        command_name = command_file[:-3] # Remove '.py' extension
        command_module = import_module(f'commands.{command_name}')

        # Assume each command has a function corresponding to the command
        command_function: CommandResponse = getattr(command_module, command_name)

        # Register the event handler
        @client.on(events.NewMessage(pattern=f'(?i)^/{command_name}(?:@(\\w+))?'))  # Trigger on command like /auction
        async def handler(event, command_file=command_file, command_function=command_function): # Pass command_function and _file else no workey
            try:
                now = time() # telegram doesn't store ms, so this does not work event.date.isoformat() so we use this custom one

                mention = event.pattern_match.group(1)
                if mention is not None and mention != 'xcuionuswjbhrahv_bot' and mention != 'Pokehunt_xyz_bot':
                    # Make sure we do not trigger on for example `/info@MissRose_bot`
                    return

                # If from bot, then ignore
                user = await event.get_sender()
                await ignore_bot(user)

                cmdRes = await command_function(event, client, now)
                await event.reply(cmdRes['content'], file=cmdRes['files'][0] if cmdRes['files'] else None, buttons=cmdRes['buttons'] if cmdRes['buttons'] else None)
            except APIError as e:
                cmdRes = await parse_command_response(client, { 'embeds': [{ 'title': '❌ Error!', 'color': '#FF0000', 'description':  str(e) + '. Please contact support here: https://t.me/pokehunt_xyz'}], 'files': [], 'buttons': [], 'menus': [] })
                await event.reply(cmdRes['content'])
            except IgnoreError:
                return
            except ForbiddenError as e:
                if str(e) == 'You can\'t write in this chat (caused by SendMessageRequest)' or str(e) == 'You can\'t write in this chat (caused by SendMediaRequest)':
                    pass # Bot does not have permission to send a message in chat
                elif str(e) == 'RPCError 403: CHAT_SEND_PHOTOS_FORBIDDEN (caused by SendMediaRequest)':
                    await event.reply('I do not have permissions to send images (of Pokémon) in here. Please make sure to give this to me!')
                else:
                    print('.....')
                    print(f'An unknown ForbiddenError happened in index.py: {command_file}')
                    print(f'Exception Type: {type(e)}')
                    print(f'Exception Message: {str(e)}')
                    print('.....')
                    await event.reply('Please make sure I have enough permissions to send messages and images (of Pokémon) in here!')
            except Exception as e:
                print('---')
                print(f'An unknown error happened in index.py: {command_file}')
                print(f'Exception Type: {type(e)}')
                print(f'Exception Message: {str(e)}')
                print('---')
                cmdRes = await parse_command_response(client, { 'embeds': [{ 'title': '❌ Error!', 'color': '#FF0000', 'description': 'An unkown error occurred (client). Please contact support here: https://t.me/pokehunt_xyz'}], 'files': [], 'buttons': [], 'menus': [] })
                await event.reply(cmdRes['content'])

def load_events():
    event_files = [
        f
        for f in listdir(join(dirname(abspath(__file__)), 'events'))
        if f.endswith('.py') and f != '__init__.py'
    ]

    for event_file in event_files:
        # Dynamically load the event module
        event_name = event_file[:-3] # Remove '.py' extension
        event_module = import_module(f'events.{event_name}')

        # Assume each event has a function corresponding to the event
        event_function = getattr(event_module, event_file[:-3])

        # To make @client.on works, we check if there exists an events[event_name]
        event_type = getattr(events, event_name, None)

        # Register the event handler
        if event_type:
            @client.on(event_type())
            async def handler(event, event_function=event_function): # Pass event_function else no workey
                await event_function(event, client)

async def main():
    load_commands()
    load_events()

    await client.start()
    await client.catch_up()

    # Create WS connection (in background)
    ws_task = create_task(create_ws_connection(client))

    # DO THIS AFTER CREATING WS CONNECTION, AS IT TAKES A WHILE
    await chat_change(client, 'added', -1002302871573, 'FORCE SYNC OF COUNT TO MAKE SURE BOTINFO IS CORRECT')

    # Run the bot forever
    await ws_task

with client:
    print('Restarted!')
    client.loop.run_until_complete(main())
