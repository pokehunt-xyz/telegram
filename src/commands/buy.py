from utils.api import run_command
from utils.typess import CommandResponse

async def buy(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    id = ' '.join(args)

    return await run_command(
        client,
        event,
        now,
        'buy',
        { 'id': id },
    )
