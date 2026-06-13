# List member attendance

In this example, it will be demonstrated how to count how many times each member attended a specific activity since a given date.

The following logical steps are performed:

- Define the `team_id`, `activity_name`, and `since_date` date.
- Retrieve the team members.
- Retrieve activities from the `since_date` date and count members marked as `Attending` for matching activities.
- Print each member with their attendance count.

```py linenums="1"
--8<-- "docs_src/list_member_attendance.py"
```
