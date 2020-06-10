FROM alpine

RUN apk add curl jq
COPY ./run.sh /
ENTRYPOINT ["/run.sh"]
