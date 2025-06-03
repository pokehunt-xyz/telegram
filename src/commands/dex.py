from utils.api import run_command
from utils.general import to_int_or_none
from utils.typess import CommandResponse

async def dex(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    if len(args) == 0:
        args.insert(0, 'search')
    subcommand = args.pop(0).lower()

    if subcommand == 'edit-wishlist':
        name = ' '.join(args)

        return await run_command(
            client,
            event,
            now,
            'dex edit-wishlist',
            { 'name': name },
        )
    elif subcommand == 'view-wishlist':
        page = args[0] if len(args) > 0 else None

        return await run_command(
            client,
            event,
            now,
            'dex view-wishlist',
            { 'page': to_int_or_none(page) },
        )
    elif subcommand == 'help':
        return await run_command(
            client,
            event,
            now,
            'help',
            { 'command': 'dex' },
        )
    else:
        # Allow for /dex bulbasaur without needing the search subcommand
        if not subcommand == 'search':
            args.insert(0, subcommand)
        name = ' '.join(args)

        return await run_command(
            client,
            event,
            now,
            'dex search',
            { 'name': name },
        )
