from utils.api import run_command
from utils.typess import CommandResponse

async def leaderboard(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    category = args[0] if len(args) > 0 else None

    return await run_command(
        client,
        event,
        now,
        'leaderboard',
        { 'category': category },
    )
