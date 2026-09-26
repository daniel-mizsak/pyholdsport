# List late activity cancellations

In this example, it will be demonstrated how to list everyone who signed off from an activity during the last two hours right before it started.

The following logical steps are performed:

- Define the `team_id` and `activity_id`.
- Retrieve the activity and calculate the start of the two-hour cancellation window.
- Retrieve the users associated with the activity.
- Select users whose status is `Not attending` and whose response was updated within the cancellation window.
- Print the users in the order they signed off.

The example uses `updated_at` as the sign-off time. This field represents the last time the activity-user record was updated, so the example assumes that its latest update was the attendance response.

```py linenums="1"
--8<-- "docs_src/advanced_examples/list_late_activity_cancellations.py"
```
