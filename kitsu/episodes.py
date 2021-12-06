from .utils import return_if_error
from datetime import datetime
from .title import Titles


class AnimeEpisode:
    def __init__(self, data: dict):
        self._data = data

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
            self._data["attributes"]["titles"],
            self._data["attributes"]["canonicalTitle"],
            self._data["attributes"]["abbreviatedTitles"],
        )
