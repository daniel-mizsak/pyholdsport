# Get coaches attending activity

In this complex example, it will be demonstrated how to generate a list of coaches attending a specific activity.

The following logical steps are performed:

- Obtain the `activity_id` for the next activity with the specified name.
- Retrieve the list of `users` attending that activity.
- Since the role of the user is not included under the activity's information, fetch each user's member details to determine their role.

```py linenums="1"
--8<-- "docs_src/get_coaches_attending_activity.py"
```

1. In practice, if the list of coaches and assistants rarely changes, their member ids could be hard-coded to avoid additional API calls.
