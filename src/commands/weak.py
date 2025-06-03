from utils.api import run_command
from utils.typess import CommandResponse

async def weak(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    argument = ' '.join(args) # Pokémon name or ID or type

    return await run_command(
        client,
        event,
        now,
        'weak',
        { 'argument': argument },
    )
