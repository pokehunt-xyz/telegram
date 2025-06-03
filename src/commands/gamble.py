from utils.api import run_command
from utils.general import get_username, to_int_or_none
from utils.typess import CommandResponse

async def gamble(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]

    hunterTo = None
    if event.message.reply_to_msg_id:
        replied_message = await event.get_reply_message()
        hunterTo = replied_message.sender

    amount = ' '.join(args)

    return await run_command(
        client,
        event,
        now,
        'gamble',
        {
            'amount': to_int_or_none(amount),
            'taggedPlatform': 'telegram',
            'taggedID': str(hunterTo.id) if hunterTo else None,
            'taggedName': get_username(hunterTo) if hunterTo else None,
        }
    )
