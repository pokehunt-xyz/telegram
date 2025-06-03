from telethon.tl.types import PeerUser

from utils.api import run_command
from utils.general import to_int_or_none
from utils.typess import CommandResponse

async def donate(event, client, now) -> CommandResponse:
    if not isinstance(event.peer_id, PeerUser):
        return { 'content': 'You can only run this command in a private PM', 'embeds': [], 'files': [], 'buttons': [] }

    args = event.message.text.split()[1:]
    amount = args[0] if len(args) > 0 else None

    return await run_command(
        client,
        event,
        now,
        'donate',
        { 'amount': to_int_or_none(amount) }
    )
