from collections import namedtuple

Titles = namedtuple(
    "Title", ["en", "en_ja", "ja_jp", "canonical_title", "abbreviated_titles"]
)

simple_image = namedtuple(
    "Image", ["tiny", "large", "small", "medium", "original", "meta"]
)
