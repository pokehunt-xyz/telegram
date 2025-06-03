from utils.api import run_command
from utils.general import to_int_or_none
from utils.typess import CommandResponse

async def team(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    if len(args) == 0:
        args.insert(0, 'view')
    subcommand = args.pop(0).lower()

    if subcommand == 'view':
        page = to_int_or_none(args[-1]) if len(args) > 0 else None

        return await run_command(
            client,
            event,
            now,
            'team view',
            { 'page': page },
        )
    else:
        # Allow for /team without needing the view subcommand
        if not subcommand == 'create':
            args.insert(0, subcommand)

        name = ' '.join(args)

        return await run_command(
            client,
            event,
            now,
            'team create',
            { 'name': name },
        )
