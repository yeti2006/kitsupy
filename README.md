# kitsu
A work-in-progress asynchronous API wrapper around kitsu.io

## Usage:
```py
import asyncio
import kitsu

client = kitsu.Client()

async def main():
    anime = client.get_anime("Kimi no na wa", limit=1) 

    print(anime.title.en)

    