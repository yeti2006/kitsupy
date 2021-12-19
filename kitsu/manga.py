<<<<<<< HEAD
from .utils import return_if_error


class Manga(object):
    def __init__(self, _data: dict, cls, links=None):
        ...
=======
import datetime
from .utils import return_if_error
from ._namedtuples import Titles

class Manga(object):
    def __init__(self, data: dict, cls, links=None):
        self._data = data
        self._cls = cls
        self._links = links

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
            self._data["attributes"]["titles"].get("en", None),
            self._data["attributes"]["titles"].get("en_ja", None),
            self._data["attributes"]["titles"].get("ja_jp", None),
            self._data["attributes"].get("canonicalTitle", None),
            self._data["attributes"].get("abbreviatedTitles", None),
        )                                    

    @property
    @return_if_error()
    def volume_number(self) -> int:
        return self._data["attributes"]["volumeNumber"]  

    @property
    @return_if_error()
    def published(self) -> str:
        return datetime.datetime(self._data["attributes"]["published"].split()[0])

    @property
    @return_if_error()
    def length(self) -> str:
        return self._data["attributes"]["length"]         
>>>>>>> d4ea2c2b6c73acb6b8364d312740529215c7d10f
