# Get activity

To get a specific activity for a team, use the [`get_activity`](../reference/holdsport.md#pyholdsport.Holdsport.get_activity) method:

```py linenums="1"
--8<-- "docs_src/basic_examples/get_activity.py"
```

1. Returns `None` if a successful response contains no activity data. HTTP errors, including 404, raise `httpx2.HTTPStatusError`.

Learn more about the [`HoldsportActivity`](../reference/models.md#pyholdsport.HoldsportActivity) object.
