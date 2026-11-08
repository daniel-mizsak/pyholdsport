# Get member

To get a specific member of a team, use the [`get_member`](../reference/holdsport.md#pyholdsport.Holdsport.get_member) method:

```py linenums="1"
--8<-- "docs_src/basic_examples/get_member.py"
```

1. Returns `None` if a successful response contains no member data. HTTP errors, including 404, raise `httpx2.HTTPStatusError`.

Learn more about the [`HoldsportMember`](../reference/models.md#pyholdsport.HoldsportMember) object.
