from pyholdsport import Holdsport, HoldsportTeam

with Holdsport("username", "password") as holdsport:
    teams: list[HoldsportTeam] = holdsport.get_teams()
    for team in teams:
        print(team)
