from utils.api import run_command
from utils.typess import CommandResponse

async def help(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    command = ' '.join(args)

    return await run_command(
        client,
        event,
        now,
        'help',
        { 'command': command },
    )
