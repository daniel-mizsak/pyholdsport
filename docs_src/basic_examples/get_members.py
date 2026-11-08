from pyholdsport import Holdsport, HoldsportMember

team_id = 123

with Holdsport("username", "password") as holdsport:
    members: list[HoldsportMember] = holdsport.get_members(team_id=team_id)
    for member in members:
        print(member)
