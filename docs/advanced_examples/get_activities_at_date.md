# Get all activities at a specific date

This example collects all activities occurring on a specific date in the `activities_at_date` list. The list is empty if no activities occur that day.

The following logical steps are performed:

- Set the desired date using the `datetime` and the `ZoneInfo` modules.
- Query from the desired date, which the API includes, and retrieve each page.
- Compare start times in the chosen timezone and collect every activity on the desired date.
- Stop when a later date is reached or the API returns an empty page. This relies on activities being returned in chronological order.
- Print each matching activity's name, id, and start time.

```py linenums="1"
--8<-- "docs_src/advanced_examples/get_activities_at_date.py"
```

1. The starting date is inclusive. Querying the target date directly avoids filling the first page with earlier activities. Pagination includes matches beyond the first page.
