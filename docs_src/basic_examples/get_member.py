from pyholdsport import Holdsport, HoldsportMember

team_id = 123
member_id = 1234

with Holdsport("username", "password") as holdsport:
    # (1)!
    member: HoldsportMember | None = holdsport.get_member(
        team_id=team_id,
        member_id=member_id,
    )
    print(member)
