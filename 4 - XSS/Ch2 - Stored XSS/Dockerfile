FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV FLASK_APP=app.py

RUN apt update && apt install -y chromium

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
