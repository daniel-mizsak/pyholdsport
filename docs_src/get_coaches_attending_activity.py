from pyholdsport import Holdsport, HoldsportActivitiesUser, HoldsportActivity, HoldsportMember, HoldsportRole

holdsport = Holdsport(
    holdsport_username="username",
    holdsport_password="password",
)
team_id = 123
activity_name = "Activity Name"

activities: list[HoldsportActivity] = holdsport.get_activities(
    team_id=team_id,
    per_page=20,
)
activity_id = None
for activity in activities:
    if activity.name == activity_name:
        activity_id = activity.id
        print(f"Found activity: '{activity.name}'")
        print(f"Activity id: {activity_id}")
        print(f"Activity start time: {activity.starttime}")
        break

if activity_id is None:
    msg = f"Activity with name '{activity_name}' not found."
    raise ValueError(msg)

coaches_attending: list[str] = []
activities_users: list[HoldsportActivitiesUser] = holdsport.get_activities_users(
    activity_id,
)
for user in activities_users:
    if user.status == "Attending":
        # (1)!
        member: HoldsportMember | None = holdsport.get_member(
            team_id=team_id,
            member_id=user.user_id,
        )
        if (member is not None) and (member.role in [HoldsportRole.COACH, HoldsportRole.ASSISTANT_COACH]):
            coaches_attending.append(f"{member.firstname} {member.lastname}")

print("Coaches attending activity:")
for coach in coaches_attending:
    print(coach)
