# kitsu

> A work-in-progress asynchronous API wrapper around https://kitsu.io

⚠ This project is still under development.

---

This project is a fully featured(not at the time being) asynchronous
API Wrapper providing full functionality over the https://kitsu.io/ JSON API.

# Installation
```
Coming soon...
```

# Usage
```py
import kitsu, asyncio

client = kitsu.KitsuClient()

async def main():
    anime = client.get_anime("Kimi no na wa", limit=1)

    if anime.nsfw is False:
        print(f"{anime.title.ja_jp} is not NSFW!")

        print(f"YouTube Trailer: {anime.youtube_url}")

        print(f"Cover Art: {anime.images.cover_image_url(size="large")}")

    else:
        print(f"Oops!, this anime is {anime.age_rating} rated!")