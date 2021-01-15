FROM python:3.9.1-slim
RUN mkdir /work
WORKDIR /work
COPY main.py .
ENTRYPOINT python /work/main.py