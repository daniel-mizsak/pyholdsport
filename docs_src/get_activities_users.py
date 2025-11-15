from pyholdsport import Holdsport, HoldsportActivitiesUser

holdsport = Holdsport(
    holdsport_username="username",
    holdsport_password="password",
)
activity_id = 12345

activities_users: list[HoldsportActivitiesUser] = holdsport.get_activities_users(
    activity_id,
)
for user in activities_users:
    print(user)
