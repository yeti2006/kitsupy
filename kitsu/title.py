from .utils import decorate_class_with_decorator, return_if_error


@decorate_class_with_decorator(property)
@decorate_class_with_decorator(return_if_error())
class Titles:
    def __init__(self, titles, canonical_title, abbreviated_titles):
        self._titles = titles
        self._canonical_title = canonical_title
        self._abbreviated_titles = abbreviated_titles

    def en(self):
        return self._titles["en__"]

    def en_ja(self):
        return self._titles["en_jp"]

    def ja_jp(self):
        return self._titles["ja_jp"]

    def canonical_title(self):
        return self._canonical_title

    def abbreviated_titles(self):
        return self._abbreviated_titles or None
