FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /usr/local/bin/uv

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY . .
RUN useradd --create-home app
USER app

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "gemstone_service.main:app", "--app-dir", "services/gemstone-service/src", "--host", "0.0.0.0", "--port", "8000"]
