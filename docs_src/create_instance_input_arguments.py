from pyholdsport import Holdsport

with Holdsport(
    holdsport_username="username",
    holdsport_password="password",
) as holdsport:
    holdsport.get_teams()
