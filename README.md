# project-ml
project meta llama




## Development

**1. Install local dev environment ONLY ONCE:**

```bash
bash scripts/setup_env.sh
```

Add in new dependencies by updating `pyproject.toml` and running

```bash
uv pip install -r pyproject.toml --extra dev
```

> [!NOTE]
> Python package and project management is done with [uv](https://github.com/astral-sh/uv). It's so fast...


**2. Build & run docker:**

```bash
bash scripts/run_docker.sh
```