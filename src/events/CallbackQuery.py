from time import time

from utils.api import run_callback_command, handle_exception
from utils.general import ignore_bot

async def CallbackQuery(event, client):
    now = time()
    try:
        await event.answer()

        # If from bot, then ignore
        user = await event.get_sender()
        await ignore_bot(user)

        cmdRes = await run_callback_command(event, client, now)
        await event.edit(cmdRes['content'], file=cmdRes['files'][0] if cmdRes['files'] else None, buttons=cmdRes['buttons'] if cmdRes['buttons'] else None)
    except Exception as e:
        await handle_exception(e, event, client, 'CallbackQuery.py')
