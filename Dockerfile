FROM alpine:3.9.4
ENV APP_HOME /opt/vizix/
WORKDIR ${APP_HOME}
RUN apk update &&\
    apk add bash &&\
    apk add curl 
COPY src/run-job.sh ${APP_HOME}
ENTRYPOINT ["sh", "-c"]
CMD ["./run-job.sh"]

