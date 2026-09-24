from pyholdsport import Holdsport, HoldsportMember

with Holdsport(
    holdsport_username="username",
    holdsport_password="password",
) as holdsport:
    team_id = 123

    members: list[HoldsportMember] = holdsport.get_members(team_id=team_id)
    for member in members:
        print(member)
