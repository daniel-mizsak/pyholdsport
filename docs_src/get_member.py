from pyholdsport import Holdsport, HoldsportMember

holdsport = Holdsport(
    holdsport_username="username",
    holdsport_password="password",
)
team_id = 123
member_id = 1234

# (1)!
member: HoldsportMember | None = holdsport.get_member(
    team_id=team_id,
    member_id=member_id,
)
print(member)
