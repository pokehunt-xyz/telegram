from utils.api import run_command
from utils.general import get_entity, get_username
from utils.typess import CommandResponse

async def trade(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]
    if len(args) == 0:
        args.insert(0, 'view')
    subcommand = args.pop(0).lower()

    if subcommand == 'cancel':
        return await run_command(
            client,
            event,
            now,
            'trade cancel',
            {},
        )
    elif subcommand == 'confirm':
        return await run_command(
            client,
            event,
            now,
            'trade confirm',
            {},
        )
    elif subcommand == 'add' or subcommand == 'remove':
        item = args[0] if len(args) > 0 else None
        if item and item.lower() == 'pokémon':
            item = 'pokemon'

        # For example, if user does /trade add 3 it will ask them if they want to add 3 credits/redeems of poke with ID 3
        if not item == 'credits' and not item == 'redeems' and not item == 'pokemon':
            value = ' '.join(args[0:])
            item = 'viabutton'
        else:
            value = ' '.join(args[1:])
            if item == 'credits' or item == 'redeems':
                value = int(value)

        return await run_command(
            client,
            event,
            now,
            f'trade {subcommand}{item}',
            { 'value': value },
        )
    elif subcommand == 'view':
        return await run_command(
            client,
            event,
            now,
            'trade view',
            {},
        )
    elif subcommand == 'help':
        return await run_command(
            client,
            event,
            now,
            'help',
            { 'command': 'trade' },
        )
    else:
        # Allow for /trade @psyche64 without needing the start subcommand
        if not subcommand == 'start':
            args.insert(0, subcommand)

        if event.message.reply_to_msg_id:
            replied_message = await event.get_reply_message()
            hunterTo = replied_message.sender
            args.insert(0, None) # hunterTo is fetched from mention
        else:
            hunterToMention = args[0] if len(args) > 0 else None
            hunterTo = await get_entity(client, hunterToMention)

        return await run_command(
            client,
            event,
            now,
            'trade start',
            {
                'taggedPlatform': 'telegram',
                'taggedID': str(hunterTo.id) if hunterTo else None,
                'taggedName': get_username(hunterTo) if hunterTo else None,
            }
        )
