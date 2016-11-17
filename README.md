mailgun-send
------------

Docker image for sending emails via Mailgun. 

This version uses Consul for storing settings and sends only basic emails.

```
$ export APP_NAME=mailgun CONSUL="consul:8500"
$ curl -X PUT -d 'key-YOURAPIKEY' "http://$CONSUL/v1/kv/$APP_NAME/api_key"
$ curl -X PUT -d 'your.mail.domain.com' "http://$CONSUL/v1/kv/$APP_NAME/email_domain"
```

```
$ docker run --rm --net somewhere-with-consul symfoni/mailgun-send:latest $CONSUL $APP_NAME "to@someone.com" "Hey!!" "Just wanted to say hi. \

Give me a call." "Me <me@friend.com>"
```
