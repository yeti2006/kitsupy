import datetime
from .utils import return_if_error
from ._namedtuples import Titles
from .images import Images


class Manga(object):
    def __init__(self, data: dict, cls, links=None):
        self._data = data
        self._cls = cls
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
    def chapter_count(self) -> int:
        print(self._data["attributes"]["chapterCount"])
        return self._data["attributes"]["chapterCount"]

    @property
    @return_if_error()
    def volume_count(self) -> int:
        return self._data["attributes"]["volumeCount"]

    @property
    @return_if_error()
    def serialization(self) -> str:
        return self._data["attributes"]["serialization"]

    @property
    @return_if_error()
    def manga_type(self) -> str:
        return self._data["attributes"]["mangaType"]

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
        return [x["name"] for x in (await self._original_genres())]
