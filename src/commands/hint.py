from utils.api import run_command
from utils.typess import CommandResponse

async def hint(event, client, now) -> CommandResponse:
    return await run_command(
        client,
        event,
        now,
        'hint',
        {},
    )
