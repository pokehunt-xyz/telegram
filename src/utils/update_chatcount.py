from telethon import TelegramClient
from telethon.tl import types
from telethon.tl.functions.updates import GetDifferenceRequest

def dict_from_state(state):
    return {'pts': state.pts, 'qts': state.qts, 'date': state.date}

async def search_pts(client, state, found_pts):
    while found_pts['bottom']  <= found_pts['top']:
        state['pts'] = (found_pts['bottom'] + found_pts['top']) // 2
        try:
            response = await client(GetDifferenceRequest(**state))
        except: response = None
        if not response or isinstance(response, types.updates.DifferenceTooLong):
            found_pts['bottom'] = state['pts'] + 1
        else:
            found_pts['top'] = state['pts'] - 1
    state['pts'] = found_pts['bottom']
    return state, found_pts

async def cache_all_bot_chats(client, state, total_pts):
    found_pts = {'bottom': 0, 'top': 0}
    state, found_pts = await search_pts(client, state, found_pts)

    while True:
        try:
            response = await client(GetDifferenceRequest(**state))
            if isinstance(response, types.updates.DifferenceEmpty):
                break
            elif isinstance(response, types.updates.Difference):
                state = dict_from_state(response.state)
            elif isinstance(response, types.updates.DifferenceSlice):
                state = dict_from_state(response.intermediate_state)
            elif isinstance(response, types.updates.DifferenceTooLong):
                bottom = state['pts']
                top = response.pts
                state, found_pts = await search_pts(client, bottom, found_pts)
        except Exception as e:
            return print(f'Error getting difference: {type(e)}: {e}')
        # print(f'Fetching peers {(state["pts"] / total_pts) * 100:0.2f}%', flush=True, end='\r')
    # print('\nFinished')
    return True

async def update_entities(client):
    success = await cache_all_bot_chats(
        client,
        {'qts': 1, 'pts': 1, 'date': 1, 'pts_total_limit': 2**31 - 1},
        client._message_box.session_state()[0]['pts']
    )

    if success:
        client.session.save()



async def get_bot_dialog_ids(client) -> list[int]:
    await update_entities(client)

    return [
        en[0]
        for en in client.session._cursor()
        .execute('SELECT * FROM entities')
        .fetchall()
    ]
