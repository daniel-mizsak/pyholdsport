from pyholdsport import Holdsport, HoldsportTeam

holdsport = Holdsport(
    holdsport_username="username",
    holdsport_password="password",
)

teams: list[HoldsportTeam] = holdsport.get_teams()
for team in teams:
    print(team)
