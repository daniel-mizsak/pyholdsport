from collections import Counter
from datetime import UTC, date, datetime
from time import sleep
from zoneinfo import ZoneInfo

from pyholdsport import Holdsport, HoldsportActivityUserStatus

team_id = 123
activity_name = "Activity Name"
start_date = date(2026, 3, 9)
end_date = date(2026, 3, 14)
timezone = ZoneInfo("Europe/Copenhagen")
now = datetime.now(UTC)

with Holdsport("username", "password") as holdsport:
    members = holdsport.get_members(team_id=team_id)
    member_ids = {member.id for member in members}

    attendance_counts: Counter[int] = Counter()
    page = 1
    while True:
        if page > 1:
            sleep(1)
        activities = holdsport.get_activities(
            team_id=team_id,
            date=start_date.isoformat(),
            page=page,
            per_page=50,
        )
        if not activities:
            break

        reached_end = False
        for activity in activities:
            activity_start = datetime.fromisoformat(activity.starttime)
            if (
                activity_start > now
                or activity_start.astimezone(timezone).date() >= end_date
            ):
                # The API returns activities in chronological order.
                reached_end = True
                break

            if activity.name != activity_name:
                continue

            activities_users = holdsport.get_activities_users(
                activity_id=activity.id,
            )
            for user in activities_users:
                if (
                    user.status_code
                    is not HoldsportActivityUserStatus.ATTENDING
                ):
                    continue
                if user.user_id not in member_ids:
                    continue
                attendance_counts[user.user_id] += 1

        if reached_end:
            break
        page += 1

    print(
        f"This report counts member attendance responses for '{activity_name}' "
        f"from {start_date.isoformat()} to {end_date.isoformat()} "
        "(end date excluded):"
    )
    sorted_members = sorted(
        members,
        key=lambda member: (
            -1 * attendance_counts[member.id],
            member.lastname,
            member.firstname,
        ),
    )
    for member in sorted_members:
        member_name = f"{member.firstname} {member.lastname}"
        print(f"{member_name}: {attendance_counts[member.id]}")
