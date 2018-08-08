#!/bin/sh
if [ "heroku" = $1 ]; then
  gunicorn -b 0.0.0.0:$PORT main:app --log-file=-
else
  python3 main.py
fi
