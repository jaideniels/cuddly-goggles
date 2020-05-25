FROM python:3.7.7-buster

RUN useradd -ms /bin/bash stacks


WORKDIR /stacks

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt 
RUN venv/bin/pip install gunicorn

COPY app app
COPY stacks.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP stacks.py

RUN chown -R stacks:stacks ./

USER stacks
EXPOSE 8080
EXPOSE 5678

ENTRYPOINT ["./boot.sh"]
