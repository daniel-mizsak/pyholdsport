# Get coaches attending activity

This example lists coaches, assistants, and team leaders marked as attending the next activity with a given name.

- Search one page from today using [`get_activities`](../reference/holdsport.md#pyholdsport.Holdsport.get_activities), skipping activities that have started.
- Fetch team members once to identify the relevant roles.
- Print matching activity users marked as `Attending`.

The API returns activities in chronological order. The search raises `ValueError` if no match is found in this page. To search beyond the default 20 activities, increase `per_page` (maximum 50) or use [pagination](../basic_examples/get_activities.md#optional-pagination).

```py linenums="1"
--8<-- "docs_src/advanced_examples/get_coaches_attending_activity.py"
```
