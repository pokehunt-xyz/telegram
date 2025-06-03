from utils.api import run_command
from utils.typess import CommandResponse

async def favorite(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]

    return await run_command(
        client,
        event,
        now,
        'favorite',
        { id: ' '.join(args) },
    )
