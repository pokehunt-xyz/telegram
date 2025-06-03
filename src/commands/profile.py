from telethon.tl.types import User

from base64 import b64encode
from utils.api import run_command, parse_command_response
from utils.general import get_entity, get_username
from utils.typess import CommandResponse

async def profile(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]

    if event.message.reply_to_msg_id:
        replied_message = await event.get_reply_message()
        hunterTo = replied_message.sender
    else:
        hunterToMention = args[0] if len(args) > 0 else None
        hunterTo = await get_entity(client, hunterToMention) if hunterToMention else await event.get_sender()

    if len(args) > 0 and (args[0] == 'public' or args[0] == 'private'):
        return await parse_command_response(client, { 'content': 'Use `/settings profile` to set your profile to public/private!', 'embeds': [], 'files': [], 'buttons': [], 'menus': [] })

    if hunterTo is None or not(isinstance(hunterTo, User)):
        return await parse_command_response(client, { 'content': 'You need to tag a valid user! See `/help profile` for examples.', 'embeds': [], 'files': [], 'buttons': [], 'menus': [] })

    photos = await client.get_profile_photos(hunterTo)
    if not photos.total == 0:
        photo = photos[0]  # Most recent photo
        hunterToAvatar = b64encode(
            await client.download_media(photo, thumb=photo.sizes[0], file=bytes)
        ).decode('utf-8')
    else:
        hunterToAvatar = None

    return await run_command(
        client,
        event,
        now,
        'profile',
        {
            'taggedID': str(hunterTo.id),
            'taggedPlatform': 'telegram',
            'taggedName': get_username(hunterTo),
            'taggedAvatar': hunterToAvatar,
        },
    )
