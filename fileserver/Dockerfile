FROM python:3.12-alpine

WORKDIR /app

COPY ./ /app

RUN pip install -r requirements.txt --no-cache

# this is so uvicorn can find the modules
ENV PYTHONPATH=/app/src

EXPOSE ${API_PORT}

# install libraries
RUN apk update
RUN apk add --no-cache libmagic

CMD uvicorn --host $API_HOST --port $API_PORT src.app:app
