import httpx2
from pyholdsport import Holdsport

with httpx2.Client(timeout=60.0) as client:
    holdsport = Holdsport("username", "password", client=client)
    holdsport.get_teams()
