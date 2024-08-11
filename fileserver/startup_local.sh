#!/bin/sh

pip install debugpy && \
python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 -m uvicorn --host $API_HOST --port $API_PORT src.app:app  --reload