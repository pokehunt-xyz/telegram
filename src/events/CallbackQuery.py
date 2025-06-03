from telethon.errors.rpcbaseerrors import ForbiddenError
from time import time

from utils.api import parse_command_response, run_callback_command
from utils.error import APIError, IgnoreError
from utils.general import ignore_bot

async def CallbackQuery(event, client):
    now = time()
    try:
        await event.answer()

        # If from bot, then ignore
        user = await event.get_sender()
        await ignore_bot(user)

        cmdRes = await run_callback_command(event, client, now)
        await event.edit(cmdRes['content'], file=cmdRes['files'][0] if cmdRes['files'] else None, buttons=cmdRes['buttons'] if cmdRes['buttons'] else None)
    except APIError as e:
        cmdRes = await parse_command_response(client, { 'embeds': [{ 'title': '❌ Error!', 'color': '#FF0000', 'description': str(e) + '. Please contact support here: https://t.me/pokehunt_xyz'}], 'files': [], 'buttons': [], 'menus': [] })
        await event.edit(cmdRes['content'])
    except IgnoreError:
        return
    except ForbiddenError as e:
        if str(e) == 'You can\'t write in this chat (caused by EditMessageRequest)':
            pass # Bot does not have permission to edit a message in chat
        else:
            print('.....')
            print(f'An unknown ForbiddenError happened in CallbackQuery.py')
            print(f'Exception Type: {type(e)}')
            print(f'Exception Message: {str(e)}')
            print('.....')
            await event.reply('Please make sure I have enough permissions to send messages and images (of Pokémon) in here!')
    except Exception as e:
        print('---')
        print('An unknown error happened: CallbackQuery.py')
        print(f'Exception Type: {type(e)}')
        print(f'Exception Message: {str(e)}')
        print('---')
        cmdRes = await parse_command_response(client, { 'embeds': [{ 'title': '❌ Error!', 'color': '#FF0000', 'description': 'An unkown error occurred (client).Please contact support here: https://t.me/pokehunt_xyz'}], 'files': [], 'buttons': [], 'menus': [] })
        await event.edit(cmdRes['content'])
