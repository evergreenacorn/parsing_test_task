FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/python/app

COPY Pipfile Pipfile.lock /home/python/app/

RUN pip install pipenv && pipenv install --system

COPY ./app /home/python/app/
CMD ["/bin/bash","-c","python main.py" ]
