import aiohttp, asyncio
import typing

from .manga import Manga
from .anime import Anime
from .episodes import AnimeEpisode
from .errors import KitsuError
from .utils import return_if_error
from .character import Character

from pprint import pprint as p


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
        if isinstance(_object, list):
            _object = _object[0]

        if _object._links or _object.links:

            response = await self._request(
                endpoint=_object._links["next"], *args, **kwargs
            )

            links = response.get("links", None)

        # Implement check for object type and return instance accordingly
        if isinstance(_object, Anime):
            return (
                [Anime(x, self, links) for x in response["data"]]
                if links
                else Anime(response, self)
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
            _data = await response.json()

            if isinstance(_data["data"], dict):  # Has only returned one result
                return _data["data"]
            elif isinstance(_data["data"], list):  # Multiple results
                if (
                    len(_data["data"]) == 1
                ):  # but only one result given(this possibly would not be necessary)
                    return _data["data"][0]
                else:
                    return _data

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
        *,
        query: typing.Union[int, str],
        limit: int = 10,
        offset: int = 0,
        custom_params: dict = None,
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

        else:
            raise KitsuError(
                "Invalid Type for argument query",
                "Valid types: str, or int",
                f"Got {type(query).__name__} instead.",
            )

        response = await self._request(
            endpoint=endpoint,
            params=params,
        )

        links = response["links"].get("first", None) if response.get("links") else None
        return (
            [Anime(x, self, links) for x in response["data"]]
            if links
            else Anime(response, self)
        )

    async def trending_anime(
        self,
        *,
        limit: int = 10,
        offset: int = 0,
        custom_params: dict = None,
    ) -> Anime:

        params = (
            {"page[limit]": str(limit), "page[offset]": str(offset)}
            if not custom_params
            else custom_params
        )

        endpoint = "trending/anime"

        response = await self._request(
            endpoint=endpoint,
            params=params,
        )

        links = (
            response["links"].get("first", None)
            if response.get("links")
            else None or len(response["data"]) != 1
        )

        return (
            [Anime(x, self, links) for x in response["data"]]
            if links
            else Anime(response, self)
        )

    async def get_episode(
        self,
        *,
        query: typing.Union[int, str],
        limit: int = 10,
        offset: int = 0,
        custom_params: dict = None,
    ) -> AnimeEpisode:

        params = (
            {"page[limit]": str(limit), "page[offset]": str(offset)}
            if not custom_params
            else custom_params
        )

        endpoint = "episodes"

        if isinstance(query, int):
            endpoint = f"episodes/{query}"
        elif isinstance(query, str):
            params["filter[text]"] = query

        else:
            raise KitsuError(
                "Invalid Type for argument query",
                "Valid types: str, or int",
                f"Got {type(query).__name__} instead.",
            )

        response = await self._request(
            endpoint=endpoint,
            params=params,
        )

        links = response["links"].get("first") if response.get("links") else None
        return (
            [AnimeEpisode(x, self, links) for x in response["data"]]
            if links
            else AnimeEpisode(response, self)
        )

    async def get_character(
        self,
        *,
        query: typing.Union[int, str],
        anime: bool = False,
        manga: bool = False,
        limit: int = 10,
        offset: int = 0,
        custom_params: dict = None,
    ) -> Character:

        params = (
            {"page[limit]": str(limit), "page[offset]": str(offset)}
            if not custom_params
            else custom_params
        )

        if not anime and not manga:
            endpoint = "media-characters"
        elif anime and not manga:
            endpoint = "anime-characters"
        elif manga and not anime:
            endpoint = "manga-characters"

        if isinstance(query, int):
            endpoint = f"{endpoint}/{query}"
        else:
            raise KitsuError(
                "Invalid Type for argument query",
                "Valid types:int",
                f"Got {type(query).__name__} instead.",
            )

        response = await self._request(
            endpoint=endpoint,
            params=params,
        )

        links = response["links"].get("first", None) if response.get("links") else None
        return (
            [await Character._init(x, self, links) for x in response["data"]]
            if links
            else await Character._init(response, self)
        )

    async def get_manga(
        self,
        *,
        query: typing.Union[int, str],
        limit: int = 10,
        offset: int = 0,
        custom_params: dict = None,
    ) -> Manga:

        params = (
            {"page[limit]": str(limit), "page[offset]": str(offset)}
            if not custom_params
            else custom_params
        )

        endpoint = "manga"

        if isinstance(query, int):
            endpoint = f"manga/{query}"
        elif isinstance(query, str):
            params["filter[text]"] = query

        else:
            raise KitsuError(
                "Invalid Type for argument query",
                "Valid types: str, or int",
                f"Got {type(query).__name__} instead.",
            )

        response = await self._request(
            endpoint=endpoint,
            params=params,
        )

        links = response["links"].get("first", None) if response.get("links") else None
        return (
            [Manga(x, self, links) for x in response["data"]]
            if links
            else Manga(response, self)
        )

    async def close(self):
        """Closes the aiohttp session"""

        return await self._session.close()
