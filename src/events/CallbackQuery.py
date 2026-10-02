from telethon.errors import WebpageCurlFailedError
from time import monotonic, time

from utils.api import run_callback_command, handle_exception
from utils.general import ignore_bot

# We only allow one callback per user per message
active_callbacks: set[tuple[int, int, int]] = set()

# We only allow one callback per user per COOLDOWN seconds, to prevent spam
COOLDOWN = 0.2
last_callbacks: dict[int, float] = {}

async def CallbackQuery(event, client):
    now = time()
    now_mon = monotonic()

    # If from bot, then ignore
    user = await event.get_sender()
    await ignore_bot(user)

    key = (
        event.chat_id,
        event.message_id,
        user.id,
    )

    # If this user already has pressed a button on this message, then ignore it
    if key in active_callbacks:
        return

    # If this user has pressed a button in the last 0.5 seconds, then ignore it
    if user.id in last_callbacks and now_mon - last_callbacks[user.id] < COOLDOWN:
        return

    active_callbacks.add(key)
    last_callbacks[user.id] = now_mon

    try:
        await event.answer()

        cmdRes = await run_callback_command(event, client, now)
        await event.edit(
            cmdRes['content'],
            file=cmdRes['files'] if cmdRes['files'] else None,
            buttons=cmdRes['buttons'] if cmdRes['buttons'] else None
        )
    except WebpageCurlFailedError:
        await event.edit(
            cmdRes['content'],
            buttons=cmdRes['buttons'] if cmdRes['buttons'] else None
        )
    except Exception as e:
        await handle_exception(e, event, client, 'CallbackQuery.py')
    finally:
        active_callbacks.discard(key)
