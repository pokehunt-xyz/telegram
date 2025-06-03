from utils.api import run_command
from utils.general import to_int_or_none
from utils.typess import CommandResponse

async def pokemon(event, client, now) -> CommandResponse:
    args = event.message.text.split()[1:]

    page = to_int_or_none(args[-1]) if len(args) > 0 else None
    if page is None:
        pokenameInput = ' '.join(args)
    elif len(args) == 0:
        pokenameInput = None
    else:
        pokenameInput = ' '.join(args[:-1])

    if pokenameInput.lower().startswith('shiny '):
        pokenameInput = pokenameInput[6:]
        shiny = True
    else:
        shiny = None

    return await run_command(
        client,
        event,
        now,
        'pokemon',
        {
            'page': to_int_or_none(page),
            'fbs': {
                'filters': {
                    'name': pokenameInput,
                    'shiny': shiny,
                },
            },
        },
    )
