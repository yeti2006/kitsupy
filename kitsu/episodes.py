from .utils import return_if_error
from datetime import datetime
from .title import Titles


class AnimeEpisode(object):
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
        print(self._data)
        return Titles(
            self._data["attributes"]["titles"],
            self._data["attributes"]["canonicalTitle"],
            self._data["attributes"]["abbreviatedTitles"],
        )

    @property
    @return_if_error()
    def season_number(self) -> int:
        return self._data["attributes"]["seasonNumber"]

    @property
    @return_if_error()
    def number(self) -> int:
        return self._data["attributes"]["number"]

    @property
    @return_if_error()
    def relative_number(self) -> int:
        return self._data["attributes"]["relativeNumber"]

    @property
    @return_if_error()
    def airdate(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["airdate"])

    @property
    @return_if_error()
    def length(self) -> int:
        return self._data["attributes"]["length"]

    @property
    @return_if_error()
    def thumbnail_url(self) -> str:
        return self._data["attributes"]["thumbnail"]["original"]
