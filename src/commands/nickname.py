from utils.api import run_command
from utils.general import to_int_or_none
from utils.typess import CommandResponse

async def nickname(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    id = to_int_or_none(args[0]) if len(args) > 0 else None
    if id is None:
        nickname = ' '.join(args)
    elif len(args) == 0:
        nickname = None
    else:
        nickname = ' '.join(args[1:])

    return await run_command(
        client,
        event,
        now,
        'nickname',
        {
            'id': id,
            'nickname': nickname,
        },
    )
