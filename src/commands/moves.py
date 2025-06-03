from utils.api import run_command
from utils.typess import CommandResponse

async def moves(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    id = ' '.join(args) # Pokémon name or ID

    return await run_command(
        client,
        event,
        now,
        'moves',
        {
            'id': id,
            'page': 1
        },
    )
