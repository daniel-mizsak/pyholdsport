# Get activities on a specific date

This example collects activities for one calendar day.

- Pass the desired `date` to [`get_activities`](../reference/holdsport.md#pyholdsport.Holdsport.get_activities).
- Collect matching activities, stopping at the first later date.
- Print each activity's name, id, and local start time.

The API returns activities in chronological order. This example checks one page (20 activities by default). For more results, increase `per_page` (maximum 50) or use [pagination](../basic_examples/get_activities.md#optional-pagination).

```py linenums="1"
--8<-- "docs_src/advanced_examples/get_activities_at_date.py"
```
