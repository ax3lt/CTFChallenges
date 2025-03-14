FROM python:3.9

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    chromium \
    libxss1 \
    libnss3 \
    libxshmfence1 \
    libatk-bridge2.0-0 \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    --no-install-recommends

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x start.sh

EXPOSE 80

CMD ["./start.sh"]
