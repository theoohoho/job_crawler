FROM python:3.7.9-slim-buster
LABEL author="theoohoho"

RUN apt update
RUN apt install -y vim
RUN mkdir /job_crawler
COPY ./ /job_crawler/
WORKDIR /job_crawler
RUN pip install -r requirements.txt
RUN . ./setup.sh

CMD ["python", "main.py", "--yourattor", "--keyword", "python", "--interval", "60"]
