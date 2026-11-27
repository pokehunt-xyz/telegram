from functools import cache
from os import getenv
from telethon.tl.types import Channel
from time import monotonic

from utils.error import IgnoreError

async def get_entity(client, entity):
    try:
        return await client.get_entity(entity)
    except Exception as e:
        return None

def get_username(user):
    if user.first_name:
        return user.first_name
    else:
        return user.username

def parse_boolean(text):
    if isinstance(text, bool):
        return text
    elif isinstance(text, str):
        text = text.strip().lower()
        if text in ['true', '1', 't', 'y', 'yes']:
            return True
        elif text in ['false', '0', 'f', 'n', 'no']:
            return False
    elif isinstance(text, int):
        if text == 0:
            return False
        elif text == 1:
            return True

    return None

def to_int_or_none(value):
    if isinstance(value, int):
        return value
    try:
        if value == None:
            return None
        elif value.lstrip('-').isdigit():
            return int(value)
        else:
            return None
    except:
        return None

@cache
def allowed_chat_ids() -> set[int] | None:
    """
    The env variable ALLOWED_CHAT_IDS (e.g. for the beta bot): the bot only works in DMs and in these chats (comma separated), and leaves every other chat
    Not set (or empty): no limit. Read on first use, so after load_dotenv()
    """
    return {int(chat_id) for chat_id in getenv('ALLOWED_CHAT_IDS', '').split(',') if chat_id.strip()} or None

LEAVE_MESSAGE = (
    'This PokéHunt bot is only for testing and works in its test chat only. '
    'Add the main bot to this chat instead: https://t.me/Pokehunt_xyz_bot?startgroup=true'
)

# Chats we left recently, so we only send the message once (a command triggers both the command and the NewMessage handler)
left_chats: dict[int, float] = {}
LEFT_CHAT_MEMORY = 60 # seconds

def is_forbidden_chat(event) -> bool:
    """Whether the bot should not be in this chat (ALLOWED_CHAT_IDS is set, and this is neither a DM nor an allowed chat)"""
    allowed = allowed_chat_ids()
    return allowed is not None and not event.is_private and event.chat_id not in allowed

async def leave_chat(client, chat_id: int):
    """Send the message to add the main bot instead, and leave the chat"""
    now = monotonic()
    for old_chat_id, left_at in list(left_chats.items()):
        if now - left_at > LEFT_CHAT_MEMORY:
            del left_chats[old_chat_id]
    if chat_id in left_chats:
        return
    left_chats[chat_id] = now

    try:
        await client.send_message(chat_id, LEAVE_MESSAGE, link_preview=False)
    except Exception:
        pass # e.g. no permission to send messages, we still leave

    try:
        await client.delete_dialog(chat_id) # leaves the group/channel
    except Exception as e:
        print(f'Could not leave chat {chat_id}: {type(e)} {e}')

async def chat_guard(event, client):
    """In a chat where the bot should not be (see ALLOWED_CHAT_IDS): leave the chat, and stop handling this event (IgnoreError)"""
    if is_forbidden_chat(event):
        await leave_chat(client, event.chat_id)
        raise IgnoreError()

async def ignore_bot(user):
    if user is None:
        raise IgnoreError()
    elif isinstance(user, Channel):
        raise IgnoreError()
    elif user.bot:
        raise IgnoreError()
