from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from pyholdsport import (
    Holdsport,
    HoldsportActivityUserStatus,
    HoldsportRole,
)

team_id = 123
activity_name = "Activity Name"
timezone = ZoneInfo("Europe/Copenhagen")
coach_roles = {
    HoldsportRole.COACH,
    HoldsportRole.ASSISTANT_COACH,
    HoldsportRole.TEAM_LEADER,
}
now = datetime.now(UTC)

with Holdsport("username", "password") as holdsport:
    activity_id = None
    # This fetches one page.
    # Increase per_page or loop over page for more activities.
    for activity in holdsport.get_activities(
        team_id=team_id,
        date=now.astimezone(timezone).date().isoformat(),
    ):
        if activity.name != activity_name:
            continue
        activity_start = datetime.fromisoformat(activity.starttime)
        if activity_start <= now:
            continue

        # The API returns activities in chronological order.
        activity_id = activity.id
        activity_start_local = activity_start.astimezone(timezone)
        activity_start_time = activity_start_local.isoformat()
        print(f"Activity name: '{activity.name}'")
        print(f"Activity id: {activity_id}")
        print(f"Activity start time: {activity_start_time}")
        break

    if activity_id is None:
        msg = f"Upcoming activity '{activity_name}' was not found."
        raise ValueError(msg)

    members = holdsport.get_members(team_id=team_id)
    coach_ids = set()
    for member in members:
        if member.role in coach_roles:
            coach_ids.add(member.id)

    coaches_attending: list[str] = []
    activities_users = holdsport.get_activities_users(
        activity_id=activity_id,
    )
    for user in activities_users:
        if user.status_code is not HoldsportActivityUserStatus.ATTENDING:
            continue
        if user.user_id not in coach_ids:
            continue
        coaches_attending.append(user.name)

    print("Coaches, assistant coaches, and team leaders attending:")
    for coach in coaches_attending:
        print(coach)
