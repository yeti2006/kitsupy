from .utils import return_if_error


class Titles(object):
    def __init__(self, titles, canonical_title, abbreviated_titles):
        self._titles = titles
        self._canonical_title = canonical_title
        self._abbreviated_titles = abbreviated_titles

    @property
    @return_if_error()
    def en(self):
        return self._titles["en"]

    @property
    @return_if_error()
    def en_ja(self):
        return self._titles["en_jp"]

    @property
    @return_if_error()
    def ja_jp(self):
        return self._titles["ja_jp"]

    @property
    @return_if_error()
    def canonical_title(self):
        return self._canonical_title

    @property
    @return_if_error()
    def abbreviated_titles(self):
        return self._abbreviated_titles or None
