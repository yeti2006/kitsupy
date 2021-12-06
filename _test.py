import asyncio
from kitsu.client import KitsuClient
from pprint import pprint as p

client = KitsuClient()


async def this():

    anime = await client.get_anime("Kimi no na wa", limit=10, offset=5)

    print(len(anime))

    for x in anime:
        print(x.id)

    anime2 = await client.next(anime[0])

    print("2 ->", len(anime2))

    for y in anime2:
        print(y.id)

    await client.close()


asyncio.get_event_loop().run_until_complete(this())
