import ytmusicapi
from dotenv import load_dotenv

ytmusic = ytmusicapi.YTMusic()

def configure_env():
    load_dotenv()