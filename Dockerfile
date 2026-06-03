FROM python:3.13.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin

WORKDIR /app

ENV PATH="/app/.env/bin:$PATH"

COPY "pyproject.toml" "uv.lock" ".python-version" ./

RUN uv sync --locked

COPY pipeline/pipeline.py pipeline.py

ENTRYPOINT ["uv", "run", "python", "pipeline.py"]