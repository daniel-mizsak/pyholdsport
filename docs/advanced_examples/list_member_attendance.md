# List member attendance

This example counts `Attending` responses for current team members within a date range.

- Fetch the current members, including all roles.
- Fetch pages with [`get_activities`](../reference/holdsport.md#pyholdsport.Holdsport.get_activities) from `start_date`, stopping on an empty page, at `end_date` (exclusive), or at the first future activity.
- Count responses for activities with the specified name.
- Print members by descending count, including zeros.

The API returns activities in chronological order. Activities in progress count. Former members are excluded. Counts represent responses, not verified attendance.

The example requests 50 activities per page, with a one-second pause between pages. Each matching activity also requires a request for its attendance responses.

```py linenums="1"
--8<-- "docs_src/advanced_examples/list_member_attendance.py"
```
