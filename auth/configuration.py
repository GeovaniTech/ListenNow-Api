import ytmusicapi
from auth.headers import headers


credentials = ytmusicapi.setup(filepath="browser.json", headers_raw=headers)
ytmusic = ytmusicapi.YTMusic(credentials)