from utils.api import run_command
from utils.general import to_int_or_none
from utils.typess import CommandResponse

async def dex(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    name = ' '.join(args)

    return await run_command(
        client,
        event,
        now,
        'dex',
        { 'name': name },
    )
