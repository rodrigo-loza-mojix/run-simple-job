FROM python:3.7-slim
ENV APP_HOME=/opt/ \
    PYTHONUNBUFFERED=1
WORKDIR ${APP_HOME}
RUN apt-get update &&\
    apt-get install curl jq -y
RUN pip3 install requests pyyaml
COPY src/run-job.py ${APP_HOME}
ENTRYPOINT ["python", "/opt/run-job.py"]

