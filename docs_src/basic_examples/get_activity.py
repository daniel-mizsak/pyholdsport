from pyholdsport import Holdsport, HoldsportActivity

team_id = 123
activity_id = 12345

with Holdsport("username", "password") as holdsport:
    # (1)!
    activity: HoldsportActivity | None = holdsport.get_activity(
        team_id=team_id,
        activity_id=activity_id,
    )
    print(activity)
