from json import dumps
from time import time

from utils.api import parse_command_response, run_command, user_sent_message
from utils.error import IgnoreError
from utils.general import get_username, ignore_bot

async def NewMessage(event, client):
    now = time()

    try:
        # If from bot, then ignore
        user = await event.get_sender()
        await ignore_bot(user)

        await user_sent_message(user.id, get_username(user), event.chat_id)

        if user.id == 5774545371 and event.message.text.startswith('/admin'):
            try:
                cmdRes = await run_command(
                    client,
                    event,
                    now,
                    'admin',
                    {  'message': event.message.text }
                )
                await event.reply(cmdRes['content'], file=cmdRes['files'][0] if cmdRes['files'] else None, buttons=cmdRes['buttons'] if cmdRes['buttons'] else None)
            except Exception as e:
                cmdRes = await parse_command_response(client, { 'embeds': [{ 'title': '❌ Error!', 'color': '#FF0000', 'description': e }], 'files': [], 'buttons': [], 'menus': [] })
                await event.reply(cmdRes['content'])
    except IgnoreError:
        return
