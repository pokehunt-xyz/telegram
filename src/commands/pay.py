from utils.api import run_command
from utils.general import get_username
from utils.general import to_int_or_none
from utils.typess import CommandResponse

async def pay(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]

    hunterTo = None
    if event.message.reply_to_msg_id:
        replied_message = await event.get_reply_message()
        hunterTo = replied_message.sender

    amount = args[0] if len(args) > 0 else None
    currency = args[1] if len(args) > 1 else None

    return await run_command(
        client,
        event,
        now,
        'pay',
        {
            'amount': to_int_or_none(amount),
            'currency': currency,
            'taggedPlatform': 'telegram',
            'taggedID': str(hunterTo.id) if hunterTo else None,
            'taggedName': get_username(hunterTo) if hunterTo else None,
        },
    )
