from datetime import datetime
from zoneinfo import ZoneInfo

from pyholdsport import Holdsport, HoldsportActivity

timezone = ZoneInfo("Europe/Copenhagen")

with Holdsport(
    holdsport_username="username",
    holdsport_password="password",
) as holdsport:
    team_id = 123
    activity_date = datetime(2026, 3, 13, tzinfo=timezone).date()

    activities_at_date: list[HoldsportActivity] = []
    page = 1
    while True:
        activities = holdsport.get_activities(
            team_id=team_id,
            date=activity_date.isoformat(),  # (1)!
            page=page,
        )
        if not activities:
            break

        reached_later_date = False
        for activity in activities:
            start_time = datetime.strptime(
                activity.starttime, "%Y-%m-%dT%H:%M:%S%z"
            )
            start_date = start_time.astimezone(timezone).date()
            if start_date > activity_date:
                # Activities are returned in chronological order.
                reached_later_date = True
                break
            if start_date == activity_date:
                activities_at_date.append(activity)

        if reached_later_date:
            break
        page += 1

    for activity in activities_at_date:
        print(f"Activity name: '{activity.name}'")
        print(f"Activity id: {activity.id}")
        print(f"Activity start time: {activity.starttime}")
