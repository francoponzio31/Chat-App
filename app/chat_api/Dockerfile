FROM python:3.12-alpine

WORKDIR /app

COPY ./ /app

RUN pip install -r requirements.txt --no-cache

# turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# this is so gunicorn can find the modules
ENV PYTHONPATH=/app/src

EXPOSE ${API_PORT}

CMD gunicorn -w 4 -b $API_HOST:$API_PORT src.main:app
