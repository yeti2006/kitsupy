import aiohttp, asyncio
import typing
from .anime import Anime
from .episodes import AnimeEpisode
from .errors import KitsuError
from .utils import return_if_error


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

    async def next(self, _object, *args, **kwargs):
        if isinstance(_object, Anime):
            if _object._links:
                response = await self._request(
                    endpoint=_object._links["next"], *args, **kwargs
                )

                try:
                    links = response["links"]
                except (KeyError, ValueError):
                    links = None

                return (
                    [Anime(x, self, links) for x in response["data"]]
                    if not len(response["data"]) == 1
                    else Anime(response["data"][0], self)
                )

    async def _request(
        self, method: str = "get", endpoint: str = None, params: dict = None
    ):
        headers = {}
        headers["Accept"] = "application/vnd.api+json"
        headers["Content-Type"] = "application/vnd.api+json"

        if endpoint and "https://kitsu.io/api/edge/" in endpoint:
            endpoint = endpoint.replace("https://kitsu.io/api/edge/", "")

        response = await self._session._request(
            method, self._baseURL + endpoint, params=params, headers=headers
        )
        if response.status == 200:

            return await response.json()
        elif response.status == 404:
            raise KitsuError(404, "Route Not Found")
        else:
            err = await response.json()
            raise KitsuError(
                f"Response code: {response.status}",
                f"Error title: {err['errors'][0]['title']}",
                f"Error message: {err['errors'][0]['detail']}",
                f"Error code: {err['errors'][0]['code']}",
            )

    async def get_anime(
        self,
        query: typing.Union[int, str, Anime],
        limit: int = 10,
        offset: int = 0,
        custom_params: dict = None,
        _endpoint=None,
    ) -> Anime:

        params = (
            {"page[limit]": str(limit), "page[offset]": str(offset)}
            if not custom_params
            else custom_params
        )

        endpoint = "anime"

        if isinstance(query, int):
            endpoint = f"anime/{query}"
        elif isinstance(query, str):
            params["filter[text]"] = query
        elif isinstance(query, Anime):
            endpoint = f"anime/{Anime.id}"

        else:
            raise KitsuError(
                "Invalid Type for argument query",
                "Valid types: Anime, str, or int",
                f"Got {type(query).__name__} instead.",
            )

        response = await self._request(
            endpoint=endpoint,
            params=params,
        )
        try:
            links = response["links"]
        except (KeyError, ValueError):
            links = None

        return (
            [Anime(x, self, links) for x in response["data"]]
            if not len(response["data"]) == 1
            else Anime(response["data"][0], self)
        )

    async def get_episode(
        self,
        query: typing.Union[int, str, Anime],
        limit: int = 10,
        offset: int = 0,
        custom_params: dict = None,
    ) -> AnimeEpisode:

        pass

    async def close(self):
        """Closes the aiohttp session"""

        return await self._session.close()
