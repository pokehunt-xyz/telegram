from telethon.tl.types import Channel

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

async def ignore_bot(user):
    if user is None:
        raise IgnoreError()
    elif isinstance(user, Channel):
        raise IgnoreError()
    elif user.bot:
        raise IgnoreError()
