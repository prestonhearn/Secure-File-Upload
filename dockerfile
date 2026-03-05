FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

ENV UPLOAD_DIR=/app/uploads

RUN useradd -m appuser

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

COPY app ./app

RUN mkdir -p /app/uploads && chown -R appuser:appuser /app/uploads

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 80

CMD ["uv", "run", "uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "80"]