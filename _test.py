import asyncio
from re import X
from kitsu.client import KitsuClient
from pprint import pprint as p

client = KitsuClient()


async def this():

    anime = await client.get_anime("kimi no na wa", 3, 3)

    print([x.title for x in anime])

    # for _anime in anime:
    #     print(_anime.title.en)

    # next_anime = await client.next(anime)

    # for _anime in next_anime:
    #     print(_anime.title.en)

    await client.close()


asyncio.get_event_loop().run_until_complete(this())
