from pyholdsport import Holdsport, HoldsportActivitiesUser

activity_id = 12345

with Holdsport("username", "password") as holdsport:
    activities_users: list[HoldsportActivitiesUser] = (
        holdsport.get_activities_users(activity_id=activity_id)
    )
    for user in activities_users:
        print(user)
