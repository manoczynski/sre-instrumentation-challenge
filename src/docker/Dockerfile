FROM python:3.10.8-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

#RUN apk add build-base
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY src/ /app

#COPY src/Makefile /app/
#COPY src/setup.py /app/


RUN cd app && make prod

EXPOSE 5000

CMD ["python3", "./run.py"]

WORKDIR /app