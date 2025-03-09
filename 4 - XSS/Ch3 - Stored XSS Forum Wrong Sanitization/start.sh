#!/bin/bash
python admin_bot.py &
flask run --host=0.0.0.0 --port=80
