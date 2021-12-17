import asyncio
from re import X
from kitsu.client import KitsuClient
from pprint import pprint as p

client = KitsuClient()


async def this():

    anime = await client.get_anime("Kimi no na wa", 1)

    characters = await anime.characters()
    print([c.images.original for c in characters])

    await client.close()


asyncio.get_event_loop().run_until_complete(this())
