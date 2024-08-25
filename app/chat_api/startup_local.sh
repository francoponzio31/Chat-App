#!/bin/sh

pip install debugpy && \
python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 -m gunicorn --workers 4 --timeout 3600 --reload --log-level debug --bind $API_HOST:$API_PORT src.main:app