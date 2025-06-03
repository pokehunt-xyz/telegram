from utils.api import run_command
from utils.typess import CommandResponse

async def guide(event, client, now) -> CommandResponse:
    return await run_command(
        client,
        event,
        now,
        'guide',
        {
            'guideName': None
        },
    )
