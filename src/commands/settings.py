from utils.api import run_command, parse_command_response
from utils.general import parse_boolean
from utils.typess import CommandResponse

async def settings(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    if len(args) == 0:
        args.insert(0, 'view')
    subcommand = args.pop(0).lower()

    if subcommand == 'link':
        return await run_command(
            client,
            event,
            now,
            'settings link',
            {},
        )
    elif subcommand == 'reset':
        return await run_command(
            client,
            event,
            now,
            'settings reset',
            {},
        )
    elif subcommand == 'view':
        return await run_command(
            client,
            event,
            now,
            'settings view',
            {},
        )
    elif (
        subcommand == 'dmnotifications'
        or subcommand == 'levelup'
        or subcommand == 'profile'
    ):
        setEnabled = parse_boolean(args[0]) if len(args) > 0 else None

        return await run_command(
            client,
            event,
            now,
            f'settings {subcommand}',
            { 'setEnabled': setEnabled },
        )
    else:
        if subcommand == 'sort':
            return await parse_command_response(client, { 'content': 'This command got renamed to `/settings`!', 'embeds': [], 'files': [], 'buttons': [], 'menus': [] })

        return await run_command(
            client,
            event,
            now,
            'help',
            { 'command': 'settings', },
        )
