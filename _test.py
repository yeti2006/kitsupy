import asyncio
from kitsu.client import KitsuClient
from pprint import pprint as p

client = KitsuClient()


async def this():

    anime = await client.get_anime(
        "Kimi no na wa",
        limit=1,
    )

    print(anime.title.en)

    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(this())
