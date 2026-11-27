from telethon import events

from utils.api import chat_change
from utils.general import is_forbidden_chat, leave_chat

async def ChatAction(event, client):
    for user in await event.get_users():
        if user.is_self:
            # Leave chats where the bot should not be right away, they are not counted as a group of the bot (see ALLOWED_CHAT_IDS)
            if is_forbidden_chat(event):
                if event.user_added or event.user_joined or event.created:
                    await leave_chat(client, event.chat_id)
                return

            if event.user_added or event.user_joined or event.created: # event.created is when a new group is created and bot is added via "setup"
                await chat_change(client, 'added', event.chat_id, event.chat.title)
            elif event.user_left or event.user_kicked:
                await chat_change(client, 'removed', event.chat_id, event.chat.title)
