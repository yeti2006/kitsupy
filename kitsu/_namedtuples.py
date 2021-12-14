from collections import namedtuple

Titles = namedtuple(
    "Title", ["en", "en_ja", "ja_jp", "canonical_title", "abbreviated_titles"]
)

StreamingLinks = namedtuple(
    "Streaming_Links", ["id", "created_at", "updated_at", "url", "subs", "dubs", "links"]
)
