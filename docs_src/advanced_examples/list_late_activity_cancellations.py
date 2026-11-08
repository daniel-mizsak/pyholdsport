from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pyholdsport import (
    Holdsport,
    HoldsportActivitiesUser,
    HoldsportActivityUserStatus,
)

team_id = 123
activity_id = 12345
timezone = ZoneInfo("Europe/Copenhagen")

with Holdsport("username", "password") as holdsport:
    activity = holdsport.get_activity(
        team_id=team_id,
        activity_id=activity_id,
    )
    if activity is None:
        msg = f"The API returned no data for activity {activity_id}."
        raise ValueError(msg)

    activity_start = datetime.fromisoformat(activity.starttime)
    cancellation_window_start = activity_start - timedelta(hours=2)

    late_cancellations: list[HoldsportActivitiesUser] = []
    activities_users = holdsport.get_activities_users(
        activity_id=activity_id,
    )
    for user in activities_users:
        if user.status_code is not HoldsportActivityUserStatus.NOT_ATTENDING:
            continue
        signed_off_at = datetime.fromisoformat(user.updated_at)
        if cancellation_window_start <= signed_off_at:
            late_cancellations.append(user)

    print(f"Late cancellations for '{activity.name}':")
    for user in sorted(
        late_cancellations,
        key=lambda user: (datetime.fromisoformat(user.updated_at), user.name),
    ):
        signed_off_at = datetime.fromisoformat(user.updated_at)
        print(f"{user.name}: {signed_off_at.astimezone(timezone).isoformat()}")
