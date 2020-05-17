FROM python:3.7.5-alpine

RUN adduser -D stacks

WORKDIR /stacks

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && venv/bin/pip install -r requirements.txt \
    && venv/bin/pip install gunicorn \ 
    && apk del .build-deps gcc musl-dev

COPY app app
COPY stacks.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP stacks.py

RUN chown -R stacks:stacks ./
USER stacks

EXPOSE 5000
EXPOSE 5678

ENTRYPOINT ["./boot.sh"]
