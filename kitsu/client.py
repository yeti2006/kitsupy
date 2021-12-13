import aiohttp, asyncio
import typing
from .anime import Anime
from .episodes import AnimeEpisode
from .errors import KitsuError
from .utils import return_if_error

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

        if _object._links:

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

    # Even specifying offset returns 3000+ returns tf

    # async def next_all(self, _object, *args, **kwargs):
    #     objects = [_object]
    #     if isinstance(_object, list):
    #         _object = _object[0]

    #     while _object._links and _object._links["next"]:
    #         response = await self.next(_object)
    #         objects.append(response)
    #         return await self.next_all(response)

    #     return objects

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

        links = response.get("links", None)
        return (
            [Anime(x, self, links) for x in response["data"]]
            if links
            else Anime(response, self)
        )

    async def get_episode(
        self,
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

        links = response.get("links", None)
        return (
            [AnimeEpisode(x, self, links) for x in response["data"]]
            if links
            else AnimeEpisode(response, self)
        )

    async def close(self):
        """Closes the aiohttp session"""

        return await self._session.close()
