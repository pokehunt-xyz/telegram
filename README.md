# PokéHunt Telegram

This is the code for the official PokéHunt Telegram Bot.

## How to run the Telegram bot

Note that you need an API key to access the PokéHunt API, which you can not do (yet)

Download the file `compose.yml` from [here](https://github.com/pokehunt-xyz/telegram/blob/main/compose.yml) and edit the environment variables.

After that run the following command:

```
docker compose up -d
```

## Contributing

Pull requests are welcome. For major changes, please open a discussion first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Setup development environment

```
python -m venv ./.py-venv
./py-venv/bin/pip3 install -r requirements.txt
./py-venv/bin/mypy . --ignore-missing-imports
```
