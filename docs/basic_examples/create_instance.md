# Create a holdsport instance

Create a `Holdsport` instance with your **username** and **password**, and use it as a context manager via **with**. [Learn more about http clients here](https://pydantic.dev/docs/httpx2/advanced/clients/){target}.

```py linenums="1"
--8<-- "docs_src/basic_examples/create_instance_input_arguments.py"
```

## Using environment variables

Instead of passing credentials directly, set the `HOLDSPORT_USERNAME` and `HOLDSPORT_PASSWORD` environment variables:

```bash
export HOLDSPORT_USERNAME="username"
export HOLDSPORT_PASSWORD="password"
```

```py linenums="1"
--8<-- "docs_src/basic_examples/create_instance_environment_variables.py"
```

It is also possible to provide one value as an input argument and the other as an environment variable.

## Using a custom client

For advanced use cases, pass an existing `httpx2.Client`:

```py linenums="1"
--8<-- "docs_src/basic_examples/create_instance_custom_client.py"
```

In this case, it is the caller's responsibility to manage the client's properties and lifecycle.
