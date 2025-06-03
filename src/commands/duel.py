from telethon.tl.types import User

from utils.api import parse_command_response, run_command
from utils.general import get_entity, get_username
from utils.typess import CommandResponse

async def duel(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]

    if event.message.reply_to_msg_id:
        replied_message = await event.get_reply_message()
        hunterTo = replied_message.sender
    else:
        hunterToMention = args[0] if len(args) > 0 else None
        hunterTo = await get_entity(client, hunterToMention)

    if hunterTo and not(isinstance(hunterTo, User)):
        return await parse_command_response(client, { 'content': 'You need to tag a valid user! See `/help duel` for examples.', 'embeds': [], 'files': [], 'buttons': [], 'menus': [] })

    return await run_command(
        client,
        event,
        now,
        'duel',
        {
            'taggedPlatform': 'telegram',
            'taggedID': str(hunterTo.id) if hunterTo else None,
            'taggedName': get_username(hunterTo) if hunterTo else None,
        },
    )
