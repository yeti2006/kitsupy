import aiohttp

from .images import Images
from .title import Titles
from datetime import datetime
import typing
from .utils import return_if_error, decorate_class_with_decorator


@decorate_class_with_decorator(property)
@decorate_class_with_decorator(return_if_error())
class Anime:
    def __init__(self, data: dict):
        self._data = data

    def id(self) -> str:
        return self._data["id"]

    def type(self) -> str:
        return self._data["type"]

    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["createdAt"].strip("Z"))

    def updated_at(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["updatedAt"].strip("Z"))

    def slug(self) -> str:
        return self._data["attributes"]["slug"]

    def synopsis(self) -> str:
        return self._data["attributes"]["synopsis"]
    

    def title(self) -> Titles:
        return Titles(
            self._data["attributes"]["titles"],
            self._data["attributes"]["canonicalTitle"],
            self._data["attributes"]["abbreviatedTitles"],
        )

    def average_rating(self) -> str:
        return self._data["attributes"]["averageRating"]

    def rating_frequencies(self) -> dict:
        return self._data["attributes"]["ratingFrequencies"]

    def user_count(self) -> int:
        return self._data["attributes"]["userCount"]

    def favorites_count(self) -> int:
        return self._data["attributes"]["favoritesCount"]

    def start_date(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["startDate"])

    def end_date(self) -> datetime:
        return datetime.fromisoformat(self._data["attributes"]["endDate"])

    def popularity_rank(self) -> int:
        return self._data["attributes"]["popularityRank"]

    def rating_rank(self) -> int:
        return self._data["attributes"]["ratingRank"]

    def age_rating(self) -> str:
        return self._data["attributes"]["ageRating"]

    def age_rating_guide(self) -> str:
        return self._data["attributes"]["ageRatingGuide"]

    def subtype(self) -> str:
        return self._data["attributes"]["subtype"]

    def status(self) -> str:
        return self._data["attributes"]["status"]

    def tba(self) -> str:
        return self._data["attributes"]["tba"]

    def images(self) -> Images:
        return Images(
            self._data["attributes"]["posterImage"],
            self._data["attributes"]["coverImage"],
        )

    def episode_count(self) -> int:
        return self._data["attributes"]["episodeCount"]

    def episode_length(self) -> int:
        return self._data["attributes"]["episodeLength"]

    def youtube_id(self) -> str:
        return self._data["attributes"]["youtubeVideoId"]

    def youtube_url(self) -> str:
        return f'https://www.youtube.com/watch?v={self._data["attributes"]["youtubeVideoId"]}'

    def nsfw(self) -> bool:
        return self._data["attributes"]["nsfw"]
    
    
    