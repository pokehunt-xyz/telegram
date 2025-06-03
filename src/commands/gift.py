from utils.api import run_command
from utils.general import get_username
from utils.typess import CommandResponse

async def gift(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]

    hunterTo = None
    if event.message.reply_to_msg_id:
        replied_message = await event.get_reply_message()
        hunterTo = replied_message.sender

    id = ' '.join(args)

    return await run_command(
        client,
        event,
        now,
        'gift',
        {
            'id': id,
            'taggedPlatform': 'telegram',
            'taggedID': str(hunterTo.id) if hunterTo else None,
            'taggedName': get_username(hunterTo) if hunterTo else None,
        },
    )
