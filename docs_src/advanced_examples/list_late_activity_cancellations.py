from datetime import datetime, timedelta

from pyholdsport import (
    Holdsport,
    HoldsportActivitiesUser,
    HoldsportActivity,
    HoldsportActivityUserStatus,
)

with Holdsport(
    holdsport_username="username",
    holdsport_password="password",
) as holdsport:
    team_id = 123
    activity_id = 12345

    activity: HoldsportActivity | None = holdsport.get_activity(
        team_id=team_id,
        activity_id=activity_id,
    )
    if activity is None:
        msg = f"Activity with id {activity_id} was not found."
        raise ValueError(msg)

    activity_start = datetime.strptime(
        activity.starttime, "%Y-%m-%dT%H:%M:%S%z"
    )
    cancellation_window_start = activity_start - timedelta(hours=2)

    late_cancellations: list[tuple[HoldsportActivitiesUser, datetime]] = []
    activities_users: list[HoldsportActivitiesUser] = (
        holdsport.get_activities_users(
            activity_id=activity_id,
        )
    )
    for user in activities_users:
        signed_off_at = datetime.strptime(
            user.updated_at, "%Y-%m-%dT%H:%M:%S%z"
        )
        if (
            user.status_code is HoldsportActivityUserStatus.NOT_ATTENDING
            and cancellation_window_start <= signed_off_at < activity_start
        ):
            late_cancellations.append((user, signed_off_at))

    print(f"Late cancellations for '{activity.name}':")
    for user, signed_off_at in sorted(
        late_cancellations, key=lambda entry: (entry[1], entry[0].name)
    ):
        print(f"{user.name}: {signed_off_at.isoformat()}")
