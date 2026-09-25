import httpx2
from pyholdsport import Holdsport

with httpx2.Client(timeout=60.0) as client:
    holdsport = Holdsport(
        holdsport_username="username",
        holdsport_password="password",
        client=client,
    )
    holdsport.get_teams()
