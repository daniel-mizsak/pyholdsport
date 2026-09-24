import httpx

from pyholdsport import Holdsport

with httpx.Client(timeout=60.0) as client:
    holdsport = Holdsport(
        holdsport_username="username",
        holdsport_password="password",
        client=client,
    )
    holdsport.get_teams()
