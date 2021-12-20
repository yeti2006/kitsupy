import asyncio
from kitsu import KitsuClient
from pprint import pprint as p

client = KitsuClient()


async def this():

    m = await client.get_manga(query="One piece", limit=1)
    print(m.id)

    await client.close()


asyncio.get_event_loop().run_until_complete(this())
