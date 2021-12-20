import asyncio
from datetime import datetime

from ._namedtuples import Titles, simple_image
from .utils import return_if_error

from pprint import pprint as p


class Character(object):
    def __init__(self, _data: dict, cls, links=None):
        self._data = _data
        self._cls = cls
        self._links = links

    @classmethod
    async def _init(_cls, data, cls, links=None):
        _instance = Character(data, cls, links)
        _instance._character = await _instance._fetch_character()
        return _instance

    async def _fetch_character(self):
        response = await self._cls._request(
            endpoint=self._data["relationships"]["character"]["links"]["related"]
        )

        return response if response else None

    @property
    @return_if_error()
    def id(self) -> int:
        return self._character["id"]

    @property
    @return_if_error()
    def type(self) -> str:
        return self._character["type"]

    @property
    @return_if_error()
    def created_at(self) -> datetime:
        return datetime.fromisoformat(
            self._character["attributes"]["createdAt"].strip("Z")
        )

    @property
    @return_if_error()
    def updated_at(self) -> datetime:
        return datetime.fromisoformat(
            self._character["attributes"]["updatedAt"].strip("Z")
        )

    @property
    @return_if_error()
    def role(self) -> str:
        return self._data["attributes"]["role"]

    @return_if_error()
    async def anime(self):
        response = await self._cls._request(
            endpoint=self._data["relationships"]["anime"]["links"]["related"]
        )

        links = response["links"].get("first") if response.get("links") else None

        from .anime import Anime  # curricular import

        return (
            [Anime(x, self._cls, links) for x in response["data"]]
            if links
            else Anime(response, self._cls)
        )

    @property
    @return_if_error()
    def names(self) -> Titles:
        return Titles(
            en=self._character["attributes"]["names"].get("en", None),
            ja_jp=self._character["attributes"]["names"].get("ja_jp", None),
            en_ja=None,
            canonical_title=None,
            abbreviated_titles=None,
        )

    @property
    @return_if_error()
    def canonical_name(self) -> str:
        return self._character["attributes"]["canonicalName"]

    @property
    @return_if_error()
    def other_names(self) -> list:
        return self._character["attributes"]["otherNames"]

    @property
    @return_if_error()
    def name(self) -> str:

        return self._character["attributes"]["name"]

    @property
    @return_if_error()
    def description(self) -> str:
        return self._character["attributes"]["description"]

    @property
    @return_if_error()
    def images(self, size="original") -> simple_image:  # TEST

        return simple_image(**self._character["attributes"]["image"])
