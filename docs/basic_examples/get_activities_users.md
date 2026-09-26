# Get activities users

To list the users associated with an activity, use the [`get_activities_users`](../reference/holdsport.md#pyholdsport.Holdsport.get_activities_users) method:

```py linenums="1"
--8<-- "docs_src/basic_examples/get_activities_users.py"
```

This endpoint returns responses such as `Attending`, `Not attending`, `Available`, and `Selected`. It omits nonresponders that may appear with `Unknown` status in an activity's embedded `activities_users` list. Neither representation should be assumed to be a complete team roster.

Learn more about the [`HoldsportActivitiesUser`](../reference/models.md#pyholdsport.HoldsportActivitiesUser) object.
