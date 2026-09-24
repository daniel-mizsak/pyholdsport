from pyholdsport import Holdsport, HoldsportActivity

with Holdsport(
    holdsport_username="username",
    holdsport_password="password",
) as holdsport:
    team_id = 123

    activities: list[HoldsportActivity] = holdsport.get_activities(
        team_id=team_id,
        per_page=5,
    )
    for activity in activities:
        print(activity)
