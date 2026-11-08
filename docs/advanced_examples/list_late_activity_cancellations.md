# List late activity cancellations

This example lists users marked as `Not attending` whose response changed later than two hours before an activity started.

- Retrieve the activity and calculate the cancellation window.
- Select matching users by status and `updated_at`.
- Print names and timestamps, sorted by time and then name.

```py linenums="1"
--8<-- "docs_src/advanced_examples/list_late_activity_cancellations.py"
```
