# MiniDLNA database utilities
# used to translate MiniDLNA URLs into local: Mopidy URIs

import os
import re
import sqlite3
from pathlib import Path

import uritools


_db = None

MEDIA_URI_ID_PATTERN = re.compile(r"^/MediaItems/([0-9]*)\.[A-Za-z0-9]{2,4}$")
"""The pattern for matching the media ID from the URL path."""


def _minidlna_connect(data_dir: Path):
    global _db
    if not _db:
        print("file:" + str(data_dir / "minidlna.db") + "?mode=ro")
        _db = sqlite3.connect("file:" + str(data_dir / "minidlna.db") + "?mode=ro")
    return _db


def minidlna_lookup_path_by_url(data_dir: Path, url):
    """
    Input: http://192.168.0.2:8200/MediaItems/33198.mp3

    Output: /media/music/misc/Takeshi Furukawa - Planet of Lana (Original Soundtrack)/10 - Horizons.mp3
    """
    try:
        db = _minidlna_connect(data_dir)
        media_path = uritools.urisplit(url).path
        media_id_match = MEDIA_URI_ID_PATTERN.match(media_path)
        if media_id_match:
            media_id = media_id_match.group(1)
            for row in db.execute("SELECT PATH FROM DETAILS WHERE ID=?", (media_id, )):
                return row[0]
    except sqlite3.OperationalError:
        # any file access error
        return None
