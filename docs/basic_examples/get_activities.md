# Get activities

Use [`get_activities`](../reference/holdsport.md#pyholdsport.Holdsport.get_activities) to fetch one page: up to 20 activities from today onward by default.

Use `date` (YYYY-MM-DD) to choose the starting date. If an activity is missing, increase `per_page` (maximum 50), or fetch additional pages using `page`.

```py linenums="1"
--8<-- "docs_src/basic_examples/get_activities.py"
```

## Optional pagination

For larger searches, this recipe fetches at most five pages of 20 activities, stopping on an empty page. It waits 0.5 seconds before each additional request.

```py linenums="1"
--8<-- "docs_src/basic_examples/get_activities_paginated.py"
```

Adjust `max_pages` to suit your search. Results may be incomplete at that limit. HTTP errors propagate without retries.

Learn more about the [`HoldsportActivity`](../reference/models.md#pyholdsport.HoldsportActivity) object.
