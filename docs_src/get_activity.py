from pyholdsport import Holdsport, HoldsportActivity

holdsport = Holdsport(
    holdsport_username="username",
    holdsport_password="password",
)
team_id = 123
activity_id = 12345

# (1)!
activity: HoldsportActivity | None = holdsport.get_activity(
    team_id=team_id,
    activity_id=activity_id,
)
print(activity)
