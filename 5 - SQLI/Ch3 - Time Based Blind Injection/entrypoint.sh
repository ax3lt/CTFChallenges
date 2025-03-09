#!/bin/bash

while ! nc -z localhost 3306; do
  echo "In attesa di MySQL..."
  sleep 1
done

python init_db.py

flask run --host=0.0.0.0 --port=80
