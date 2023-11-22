FROM python:3.12-slim as base

RUN apt-get update -y && \
  apt-get install -y \
  gcc \
  curl

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction

COPY . .

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0" , "--port", "8000", "--reload"]

# devcontainer
FROM base as devcontainer

RUN apt-get install git -y
