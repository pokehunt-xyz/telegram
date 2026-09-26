from telethon.tl.types import User

from utils.api import parse_command_response, run_command
from utils.general import get_entity, get_username
from utils.typess import CommandResponse

async def stuck(event, client, now) -> CommandResponse:
    return await run_command(
        client,
        event,
        now,
        'stuck',
        {},
    )
