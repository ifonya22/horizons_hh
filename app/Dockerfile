FROM python:3.11-slim-bullseye

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# COPY .env /app

COPY . /app

CMD ["poetry", "run", "streamlit", "run", "frontend_main.py"]


# docker run -p 8501:8501 -d --name hh hh:0.0.1 