import aiohttp, asyncio
import typing
from .anime import Anime
from .errors import KitsuError


class KitsuClient:
    def __init__(self, session: typing.Optional[aiohttp.ClientSession] = None):
        self._baseURL = "https://kitsu.io/api/edge/"
        self._session = session
        if not session:
            self._session = asyncio.get_event_loop().run_until_complete(
                self._create_session()
            )

    async def _create_session(self):
        return aiohttp.ClientSession()

    async def _request(
        self, method: str = "get", endpoint: str = None, params: dict = None
    ):
        headers = {}
        headers["Accept"] = "application/vnd.api+json"
        headers["Content-Type"] = "application/vnd.api+json"

        async with getattr(self._session, method)(
            self._baseURL + endpoint, params=params, headers=headers
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                err = await response.json()
                raise KitsuError(
                    f"Response code: {response.status}",
                    f"Error title: {err['errors'][0]['title']}",
                    f"Error message: {err['errors'][0]['detail']}",
                    f"Error code: {err['errors'][0]['code']}",
                )

    async def get_anime(self, query: str, limit: int = 10, offset: int = 0) -> Anime:
        response = await self._request(
            endpoint="anime",
            params={
                "filter[text]": query,
                "page[limit]": str(limit),
                "page[offset]": str(offset),
            },
        )

        return (
            [Anime(x) for x in response["data"]]
            if not len(response["data"]) == 1
            else Anime(response["data"][0])
        )

    async def close(self):
        """Closes the aiohttp session"""

        return await self._session.close()
