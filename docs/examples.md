# Examples

## Create a holdsport instance

A `Holdsport` instance can be created by providing the username and password as input arguments:

```py linenums="1"
--8<-- "docs/snippets/create_instance_input_arguments.py"
```

Or by setting the `HOLDSPORT_USERNAME` and `HOLDSPORT_PASSWORD` environment variables:

```bash
export HOLDSPORT_USERNAME="username"
export HOLDSPORT_PASSWORD="password"
```

```py linenums="1"
--8<-- "docs/snippets/create_instance_environment_variables.py"
```

It is also possible to provide one value as an input argument and the other as an environment variable.
