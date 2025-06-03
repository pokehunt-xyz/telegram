from utils.api import run_command
from utils.typess import CommandResponse

async def botinfo(event, client, now) -> CommandResponse:
    return await run_command(
        client,
        event,
        now,
        'botinfo',
        {},
    )
