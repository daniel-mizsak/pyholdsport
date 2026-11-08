from pyholdsport import Holdsport

with Holdsport("username", "password") as holdsport:
    holdsport.get_teams()
