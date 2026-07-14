from enum import Enum

class Hosts(str, Enum):
    AUTH_URL = "https://auth.dev-cinescope.coconutqa.ru"
    MOVIES_URL = "https://api.dev-cinescope.coconutqa.ru"
