# project-ml
project meta llama




## Development

1. **Install local dev environment**

```bash
bash scripts/setup_env.sh
```

Add in new dependencies by updating `pyproject.toml` and running

```bash
bash scripts/setup_env.sh
```

or

```bash
uv pip install -r pyproject.toml --extra dev
```

> [!NOTE]
> Python package and project management is done with [uv](https://github.com/astral-sh/uv). It's so fast...

2. **Format, Lint, Type Check**

```bash
bash scripts/precommit.sh
```

3. **Build & run docker**

```bash
bash scripts/run_docker.sh
```
