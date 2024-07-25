FROM python:3.11-slim-bullseye

RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry update --no-root

RUN apt-get update && apt-get install -y supervisor


COPY supervisord.conf /etc/supervisor/supervisord.conf

EXPOSE 8502

# CMD ["poetry", "run", "streamlit", "run", "frontend_main.py"]
# CMD ["/usr/bin/supervisord"]

CMD [ "python" ]

# docker run -p 8501:8501 -d --name hh hh:0.0.1 