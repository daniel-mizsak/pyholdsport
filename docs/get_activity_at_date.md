# Get an activity at a specific date

In this slightly more complex example, it will be demonstrated how to get an activity occurring at a specific date.

The following logical steps are performed:

- Set the desired date using the `datetime` and the `ZoneInfo` modules.
- List all activities while paying attention that the `date` parameter is set to a date **before** the desired date.

```py linenums="1"
--8<-- "docs_src/get_activity_at_date.py"
```

1. This date should be before the desired date, as the API returns activities starting from the given date.
