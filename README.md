# project-ml
project meta llama




## Development

1. Install local dev environment ONLY ONCE:

```bash
bash scripts/setup_env.sh
```

Add in new dependencies by updating `pyproject.toml` and running

```bash
 pip install -e ."[dev]" 
```


2. Build & run docker:

```bash
bash scripts/run_docker.sh
```