FROM alpine:3.4
RUN apk add --no-cache curl jq bash
ADD mailgun.sh /bin/mailgun.sh
RUN chmod +x /bin/mailgun.sh
ENTRYPOINT ["/bin/mailgun.sh"]
