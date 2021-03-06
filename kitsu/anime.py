from collections import namedtuple


from .episodes import AnimeEpisode

from .images import Images
from ._namedtuples import Titles
from datetime import datetime
import typing
from .utils import return_if_error
from .character import Character

from pprint import pprint as p


class Anime(object):
    def __init__(self, data: dict, _cls, links=None):
        self._cls = _cls
        self._data = data
        self._links = links

    @property
    @return_if_error()
    def id(self) -> str:
        return self._data["id"]

    @property
    @return_if_error()
    def type(self) -> str:
        return self._data["type"]

    @property
    @return_if_error()
    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["createdAt"].strip("Z"))

    @property
    @return_if_error()
    def updated_at(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["updatedAt"].strip("Z"))

    @property
    @return_if_error()
    def slug(self) -> str:
        return self._data["attributes"]["slug"]

    @property
    @return_if_error()
    def synopsis(self) -> str:
        return self._data["attributes"]["synopsis"]

    @property
    @return_if_error()
    def title(self) -> Titles:
        return Titles(
            self._data["attributes"]["titles"].get("en"),
            self._data["attributes"]["titles"].get("en_ja"),
            self._data["attributes"]["titles"].get("ja_jp"),
            self._data["attributes"].get("canonicalTitle"),
            self._data["attributes"].get("abbreviatedTitles"),
        )

    @property
    @return_if_error()
    def average_rating(self) -> str:
        return self._data["attributes"]["averageRating"]

    @property
    @return_if_error()
    def rating_frequencies(self) -> dict:
        return self._data["attributes"]["ratingFrequencies"]

    @property
    @return_if_error()
    def user_count(self) -> int:
        return self._data["attributes"]["userCount"]

    @property
    @return_if_error()
    def favorites_count(self) -> int:
        return self._data["attributes"]["favoritesCount"]

    @property
    @return_if_error()
    def start_date(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["startDate"])

    @property
    @return_if_error()
    def end_date(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["endDate"])

    @property
    @return_if_error()
    def popularity_rank(self) -> int:
        return self._data["attributes"]["popularityRank"]

    @property
    @return_if_error()
    def rating_rank(self) -> int:
        return self._data["attributes"]["ratingRank"]

    @property
    @return_if_error()
    def age_rating(self) -> str:
        return self._data["attributes"]["ageRating"]

    @property
    @return_if_error()
    def age_rating_guide(self) -> str:
        return self._data["attributes"]["ageRatingGuide"]

    @property
    @return_if_error()
    def subtype(self) -> str:
        return self._data["attributes"]["subtype"]

    @property
    @return_if_error()
    def status(self) -> str:
        return self._data["attributes"]["status"]

    @property
    @return_if_error()
    def tba(self) -> str:
        return self._data["attributes"]["tba"]

    @property
    @return_if_error()
    def images(self) -> Images:
        return Images(
            self._data["attributes"]["posterImage"],
            self._data["attributes"]["coverImage"],
        )

    @property
    @return_if_error()
    def episode_count(self) -> int:
        return self._data["attributes"]["episodeCount"]

    @property
    @return_if_error()
    def episode_length(self) -> int:
        return self._data["attributes"]["episodeLength"]

    @property
    @return_if_error()
    def youtube_id(self) -> str:
        return self._data["attributes"]["youtubeVideoId"]

    @property
    @return_if_error()
    def youtube_url(self) -> str:
        return f'https://www.youtube.com/watch?v={self._data["attributes"]["youtubeVideoId"]}'

    @property
    @return_if_error()
    def nsfw(self) -> bool:
        return self._data["attributes"]["nsfw"]

    @property
    @return_if_error()
    async def _original_genres(self) -> list:
        _genres: dict = await self._cls._request(
            endpoint=self._data["relationships"]["genres"]["links"]["related"]
        )

        return [
            {
                "id": data["id"],
                "name": data["attributes"]["name"],
                "description": data["attributes"]["description"],
                "slug": data["attributes"]["slug"],
            }
            for data in _genres["data"]
        ]

    @property
    @return_if_error()
    async def genres(self) -> list:
        return [x["name"] for x in (await self._original_genres)]

    @return_if_error()
    async def episodes(self, limit=1):
        response = await self._cls._request(
            endpoint=self._data["relationships"]["episodes"]["links"]["related"],
            params={"page[limit]": str(limit)},
        )

        links = response["links"].get("first") if response.get("links") else None
        return (
            [AnimeEpisode(x, self, links) for x in response["data"]]
            if links
            else AnimeEpisode(response, self)
        )

    @return_if_error()
    async def streaming_links(self) -> list:
        """Streaming Links of the anime

        Returns:
            list: StreamingLinks
        """
        response = await self._cls._request(
            endpoint=self._data["relationships"]["streamingLinks"]["links"]["related"]
        )

        links = response["links"].get("first") if response.get("links") else None

        return (
            [StreamingLinks(x) for x in response["data"]]
            if links
            else StreamingLinks(response)
        )

    @return_if_error()
    async def characters(self) -> Character:
        response = await self._cls._request(
            endpoint=self._data["relationships"]["characters"]["links"]["related"]
        )

        links = response["links"].get("first") if response.get("links") else None
        return (
            [await Character._init(x, self._cls, links) for x in response["data"]]
            if links
            else await Character._init(response, self._cls)
        )

    @return_if_error()
    async def anime_characters(self) -> Character:
        response = await self._cls._request(
            endpoint=self._data["relationships"]["animeCharacters"]["links"]["related"]
        )

        links = response["links"].get("first") if response.get("links") else None

        return (
            [await Character._init(x, self._cls, links) for x in response["data"]]
            if links
            else await Character._init(response, self._cls)
        )


class StreamingLinks(object):
    def __init__(self, _data: dict, links=None):
        self._data = _data
        self._links = links

    @property
    @return_if_error()
    def id(self) -> int:
        return self._data["id"]

    @property
    @return_if_error()
    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["createdAt"].strip("Z"))

    @property
    @return_if_error()
    def updated_at(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["updatedAt"].strip("Z"))

    @property
    @return_if_error()
    def url(self) -> str:
        return self._data["attributes"]["url"]

    @property
    @return_if_error()
    def subs(self) -> list:
        return self._data["attributes"]["subs"]

    @property
    @return_if_error()
    def dubs(self) -> list:
        return self._data["attributes"]["dubs"]
