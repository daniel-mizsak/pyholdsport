from time import sleep

from pyholdsport import Holdsport

team_id = 123
max_pages = 5

with Holdsport("username", "password") as holdsport:
    for page in range(1, max_pages + 1):
        if page > 1:
            sleep(0.5)
        activities = holdsport.get_activities(team_id=team_id, page=page)
        if not activities:
            break
        for activity in activities:
            print(activity)
