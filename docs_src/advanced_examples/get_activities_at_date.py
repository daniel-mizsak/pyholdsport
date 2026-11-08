from datetime import date, datetime
from zoneinfo import ZoneInfo

from pyholdsport import Holdsport, HoldsportActivity

team_id = 123
activity_date = date(2026, 3, 13)
timezone = ZoneInfo("Europe/Copenhagen")

with Holdsport("username", "password") as holdsport:
    activities_at_date: list[HoldsportActivity] = []
    # This fetches one page.
    # Increase per_page or loop over page for more activities.
    for activity in holdsport.get_activities(
        team_id=team_id,
        date=activity_date.isoformat(),
    ):
        activity_start = datetime.fromisoformat(activity.starttime)
        start_date = activity_start.astimezone(timezone).date()
        if start_date > activity_date:
            # The API returns activities in chronological order.
            break
        if start_date == activity_date:
            activities_at_date.append(activity)

    for activity in activities_at_date:
        print(f"Activity name: '{activity.name}'")
        print(f"Activity id: {activity.id}")
        activity_start_time = (
            datetime.fromisoformat(activity.starttime)
            .astimezone(timezone)
            .isoformat()
        )
        print(f"Activity start time: {activity_start_time}")
