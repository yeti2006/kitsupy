import asyncio
from re import X
from kitsu.client import KitsuClient
from pprint import pprint as p

client = KitsuClient()


async def this():

    anime = await client.get_anime("Cowboy bepop", 1)


    streaming_links = await anime.streaming_links()
    
    for streaming_link_object in streaming_links:
        print(streaming_link_object.url)
        

    await client.close()


asyncio.get_event_loop().run_until_complete(this())
