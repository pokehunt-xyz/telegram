from utils.api import run_command
from utils.general import to_int_or_none
from utils.typess import CommandResponse

async def auction(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    if len(args) == 0:
        args.insert(0, 'help')
    subcommand = args.pop(0).lower()

    if subcommand == 'listings' or subcommand == 'my':
        page = args[0] if len(args) > 0 else None

        return await run_command(
            client,
            event,
            now,
            'auction listings',
            {
                'page': to_int_or_none(page),
                'fbs': {},
            }
        )
    elif subcommand == 'create' or subcommand == 'add' or subcommand == 'list' or subcommand == 'sell':
        minBid = to_int_or_none(args[-1]) if len(args) > 1 else None
        if minBid is None:
            pokeID = ' '.join(args)
        else:
            pokeID = ' '.join(args[:-1])

        return await run_command(
            client,
            event,
            now,
            'auction create',
            {
                'pokeID': pokeID,
                'hours': None,
                'insta': None,
                'min': minBid,
                'jump': None
            },
        )
    elif subcommand == 'bid' or subcommand == 'buy' or subcommand == 'get':
        id = args[0] if len(args) > 0 else None
        amount = args[1] if len(args) > 1 else None

        return await run_command(
            client,
            event,
            now,
            'auction bid',
            {
                'id': id,
                'amount': to_int_or_none(amount)
            },
        )
    elif subcommand == 'view' or subcommand == 'info':
        id = args[0] if len(args) > 0 else None

        return await run_command(
            client,
            event,
            now,
            'auction view',
            { 'id': id },
        )
    elif subcommand == 'end' or subcommand == 'remove':
        id = args[0] if len(args) > 0 else None

        return await run_command(
            client,
            event,
            now,
            'auction end',
            { 'id': id },
        )
    elif subcommand == 'search' or subcommand == 'find':
        page = to_int_or_none(args[-1]) if len(args) > 0 else None
        if page is None:
            pokenameInput = ' '.join(args)
        elif len(args) == 0:
            pokenameInput = None
        else:
            pokenameInput = ' '.join(args[:-1])

        if pokenameInput.lower().startswith('shiny '):
            pokenameInput = pokenameInput[6:]
            shiny = True
        else:
            shiny = None

        return await run_command(
            client,
            event,
            now,
            'auction search',
            {
                'page': page,
                'fbs': {
                    'filters': {
                        'name': pokenameInput,
                        'shiny': shiny,
                    },
                },
            },
        )
    else:
        return await run_command(
            client,
            event,
            now,
            'help',
            { 'command': 'auction' },
        )
