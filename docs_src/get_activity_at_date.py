from datetime import datetime
from zoneinfo import ZoneInfo

from pyholdsport import Holdsport, HoldsportActivity

timezone = ZoneInfo("Europe/Copenhagen")

holdsport = Holdsport(
    holdsport_username="username",
    holdsport_password="password",
)
team_id = 123
activity_date = datetime(2026, 3, 13, tzinfo=timezone).date()

activities: list[HoldsportActivity] = holdsport.get_activities(
    team_id=team_id,
    date="2026-03-10",  # (1)!
)
for activity in activities:
    start_time = datetime.strptime(activity.starttime, "%Y-%m-%dT%H:%M:%S%z")
    if start_time.date() == activity_date:
        print(f"Found activity: '{activity.name}'")
        print(f"Activity id: {activity.id}")
        print(f"Activity start time: {activity.starttime}")
        break
