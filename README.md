# kitsu

> A work-in-progress asynchronous API wrapper around https://kitsu.io

---

Asynchronous wrapper around the JSON API of [kitsu](https://kitsu.io). This project is still under development and incomplete, but usable.

## Installation

Install from github:
```py
pip install git+https://github.com/yeti2006/kitsupy 
```

## Usage

```py
import asyncio, kitsu

client = kitsu.KitsuClient() # Instantiate client;
                            # you can optionally pass your own aiohttp client session

async def main():
    anime = await client.get_anime(query="Kimi no na wa", limit=1)

    # Returns an kitsu.Anime object which happens to be the first
    # result provided by the API as limit=1

    print(anime.id) # the API based ID of the anime
    print(anime.title.en) # str, the english title of the anime
    print(anime.created_at) # a datetime.datetime object of the creation date of the anime
    print(anime.nsfw) # bool

    anime_characters = await anime.characters()

    # Returns a list of kitsu.Character objects

    for character in anime_characters:
        print(character.name)
        print(character.description)

    # Get the 10 most trending animes from the API
    trending_anime = await client.trending_anime(limit=10)

    for anime in trending_anime:
        streaming_links = await anime.streaming_links()

        for streaming_link in streaming_links:
            print(streaming_link.url) # Prints a streaming link to the anime

    # Search for a manga in API
    manga = await client.get_manga(query="One Piece", limit=1)

    print(manga.user_count) 

    await client.close() # Close our client session
```

## Documentation

The documentation can be found at:

https://yeti-is-god.ml/kitsupy

(Coming soon:tm:)

