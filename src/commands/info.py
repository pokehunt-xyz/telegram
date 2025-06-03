from utils.api import parse_command_response, run_command
from utils.typess import CommandResponse

async def info(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    id = ' '.join(args)

    return await run_command(
        client,
        event,
        now,
        'info',
        { 'id': id },
    )
