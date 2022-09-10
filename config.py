import os
from datetime import datetime

from decouple import config as dconfig

# Config settings from environment variables.
# These are treated as secrets and therefore sourced from environment variables to follow best practices.
PLAYLIST_ID = dconfig("6fd4a62380234df6")
SPOTIFY_CLIENT_ID = dconfig("f43e5da60a6744d7afddf75325e6c7b2")
SPOTIFY_CLIENT_SECRET = dconfig("827ca59efe8843f0bb79b4083e554b5d")
SPOTIFY_REDIRECT_URI = dconfig("http://localhost:8080")
SPOTIFY_USER = dconfig("Janiah Shane")


# The rest are also config settings, but their literal values are commited to the codebase since they aren't secret.

# how spotify formats dates in it's API.
spotify_date_format = "%Y-%m-%dT%H:%M:%S"
# the way I want to see it
date_format = "%Y-%m-%d %A, %I:%M %p"
spotify_scope_warning = "signing into spotify...\nIf this program or another program with the same client_id\nhas changed scopes, you'll need to reauthorize each time.\nMake sure all programs have the same scope."
scope = "playlist-modify-private, playlist-modify-public, user-library-read, playlist-read-private, user-library-modify, user-read-recently-played,user-top-read"
now_utc = datetime.now()
now_local = now_utc.astimezone()
local_offset_str = datetime.strftime(now_local, "%z")
local_offset_int = float(
    local_offset_str[:3] + (".5" if local_offset_str[3] == "3" else ".0")
)