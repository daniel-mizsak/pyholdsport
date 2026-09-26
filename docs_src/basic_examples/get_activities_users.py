from pyholdsport import Holdsport, HoldsportActivitiesUser

with Holdsport(
    holdsport_username="username",
    holdsport_password="password",
) as holdsport:
    activity_id = 12345

    activities_users: list[HoldsportActivitiesUser] = (
        holdsport.get_activities_users(
            activity_id,
        )
    )
    for user in activities_users:
        print(user)
