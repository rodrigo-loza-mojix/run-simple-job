FROM alpine:3.9.4
ENV APP_HOME=/opt/options/
WORKDIR ${APP_HOME}
RUN apk update &&\
    apk add bash curl jq &&\
    mkdir -p ${APP_HOME}/premise_codes/
COPY src/run-job.sh ${APP_HOME}
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["/opt/options/run-job.sh"]

