from utils.api import run_command
from utils.general import to_int_or_none
from utils.typess import CommandResponse

async def wishlist(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    if len(args) == 0:
        args.insert(0, 'view')
    subcommand = args.pop(0).lower()

    if subcommand == 'edit':
        name = ' '.join(args)

        return await run_command(
            client,
            event,
            now,
            'wishlist edit',
            { 'name': name },
        )
    elif subcommand == 'view':
        page = args[0] if len(args) > 0 else None

        return await run_command(
            client,
            event,
            now,
            'wishlist view',
            { 'page': to_int_or_none(page) },
        )
    else:
        return await run_command(
            client,
            event,
            now,
            'help',
            { 'command': 'wishlist' },
        )
