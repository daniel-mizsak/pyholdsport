from collections import Counter
from datetime import date, datetime

from pyholdsport import Holdsport, HoldsportActivitiesUser, HoldsportActivity, HoldsportMember

holdsport = Holdsport(
    holdsport_username="username",
    holdsport_password="password",
)
team_id = 123
activity_name = "Activity Name"
since_date = date(2026, 1, 1)

members: list[HoldsportMember] = holdsport.get_members(team_id=team_id)
member_ids: set[int] = {member.id for member in members}

attendance_counts: Counter[int] = Counter()
page = 1
while True:
    reached_future_activity = False
    activities: list[HoldsportActivity] = holdsport.get_activities(
        team_id=team_id,
        date=since_date.isoformat(),
        page=page,
        per_page=20,
    )
    if not activities:
        break

    for activity in activities:
        activity_time = datetime.strptime(activity.starttime, "%Y-%m-%dT%H:%M:%S%z")
        if activity_time > datetime.now(activity_time.tzinfo):
            # This assumes that once a future activity is reached, all subsequent activities will also be in the future.
            reached_future_activity = True
            break

        if activity.name != activity_name:
            continue

        activities_users: list[HoldsportActivitiesUser] = holdsport.get_activities_users(
            activity.id,
        )
        for user in activities_users:
            if user.status == "Attending" and user.user_id in member_ids:
                attendance_counts[user.user_id] += 1

    if reached_future_activity:
        break

    page += 1

print(f"Player attendance for '{activity_name}' since {since_date.isoformat()}:")
sorted_members = sorted(
    members,
    key=lambda member: (-attendance_counts[member.id], member.lastname, member.firstname),
)
for sorted_member in sorted_members:
    print(f"{sorted_member.firstname} {sorted_member.lastname}: {attendance_counts[sorted_member.id]}")
