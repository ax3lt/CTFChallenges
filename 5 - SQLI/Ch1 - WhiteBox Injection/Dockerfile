FROM python:3.9-slim

# Installa dipendenze di sistema e MySQL
RUN apt-get update && \
    apt-get install -y mariadb-server supervisor netcat-traditional

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh

RUN mkdir /run/mysqld

EXPOSE 80 3306

ENV FLASK_APP=app.py

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
