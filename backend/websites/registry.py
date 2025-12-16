from core.http_client import HttpJsonClient
from websites.fo1 import Fo1Website
from websites.fo2 import Fo2Website

# Factory/Registry קטן (לא להגזים)
_http = HttpJsonClient(timeout_seconds=12)

_CLIENTS = {
    "fo1.altius.finance": Fo1Website(_http),
    "fo2.altius.finance": Fo2Website(_http),
}

def get_client(website: str):
    try:
        return _CLIENTS[website]
    except KeyError:
        raise ValueError(f"Unsupported website: {website}")