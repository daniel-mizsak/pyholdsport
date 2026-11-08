from pyholdsport import Holdsport, HoldsportActivity

team_id = 123

with Holdsport("username", "password") as holdsport:
    activities: list[HoldsportActivity] = holdsport.get_activities(
        team_id=team_id,
    )
    for activity in activities:
        print(activity)
