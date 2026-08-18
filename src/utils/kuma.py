from asyncio import create_task, sleep
from aiohttp import ClientSession
from os import getenv

KUMA_PUSH_URL = getenv("KUMA_PUSH_URL")

async def uptime_kuma_ping():
    if not KUMA_PUSH_URL:
        return

    async with ClientSession() as session:
        while True:
            try:
                async with session.get(KUMA_PUSH_URL) as resp:
                    await resp.read()  # Consume response
            except Exception as e:
                print(f"Failed to ping Uptime Kuma: {e}")

            # Wait 5 minutes
            await sleep(5 * 60)