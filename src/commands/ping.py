from time import time

from utils.api import run_command
from utils.typess import CommandResponse

async def ping(event, client, now) -> CommandResponse:
    return await run_command(
        client,
        event,
        now,
        'ping',
        { 'client': int((time() - event.date.timestamp()) * 1000) }
    )
