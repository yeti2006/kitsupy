from .utils import return_if_error
import typing


class Images(object):
    def __init__(self, poster_image: dict, cover_image: dict):
        self._poster_image = poster_image
        self._cover_image = cover_image

    def poster_image_url(
        self,
        image_size: typing.Optional[
            typing.Literal["tiny", "small", "medium", "large", "original"]
        ] = "original",
    ) -> str:

        return self._poster_image.get(image_size, None)

    def poster_images(self) -> dict:
        return self._poster_image

    @return_if_error()
    def poster_image_dimensions(
        self,
        image_size: typing.Optional[
            typing.Literal["tiny", "small", "medium", "large", "original"]
        ] = None,
    ):

        if not image_size:
            return self._poster_image["meta"]["dimensions"]

        return tuple(self._poster_image["meta"]["dimensions"].get(image_size).values())

    def cover_image_url(
        self,
        image_size: typing.Optional[
            typing.Literal["tiny", "small", "medium", "large", "original"]
        ] = "original",
    ) -> str:

        return self._cover_image.get(image_size, None)

    def cover_images(self) -> dict:
        return self._cover_image

    @return_if_error()
    def cover_image_dimensions(
        self,
        image_size: typing.Optional[
            typing.Literal["tiny", "small", "medium", "large", "original"]
        ] = None,
    ):

        if not image_size:
            return self.cover_image["meta"]["dimensions"]

        return tuple(self.cover_image["meta"]["dimensions"].get(image_size).values())
