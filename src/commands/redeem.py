from utils.api import run_command
from utils.typess import CommandResponse

async def redeem(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    if len(args) == 0:
        args.insert(0, 'balance')
    subcommand = args.pop(0).lower()

    if subcommand == 'balance':
        return await run_command(
            client,
            event,
            now,
            'redeem balance',
            {},
        )
    elif subcommand == 'credits':
        return await run_command(
            client,
            event,
            now,
            'redeem credits',
            {},
        )
    elif subcommand == 'spawn':
        name = ' '.join(args)

        return await run_command(
            client,
            event,
            now,
            'redeem spawn',
            {
                'name': name,
                'autocatch': False,
                'taggedChatID': str(event.chat_id), # Telegram has no concept of "groups", so it does not make sense to spawn it in a different chat
            },
        )
    elif subcommand == 'info':
        return await run_command(
            client,
            event,
            now,
            'redeem info',
            {},
        )
    else:
        return await run_command(
            client,
            event,
            now,
            'help',
            { 'command': 'redeem' },
        )
