import asyncio
from kitsu import KitsuClient
from pprint import pprint as p

client = KitsuClient()


async def this():
    """
    :param name: session - An aiohttp client session
    :param type: str
    :return: None

    """

    animes = await client.get_anime("Kimi no na wa", limit=1)
    characters = await animes.anime_characters()
    for c in characters:
        print(c.name)

    await client.close()


asyncio.get_event_loop().run_until_complete(this())
