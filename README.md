mailgun-send
------------

Docker image for sending emails via Mailgun. 

If you are sending attachments or inline images, remember to mount them into the container.

```
$ export API_KEY=xxx EMAIL_DOMAIN=xxx"
$ docker run --rm -e API_KEY=$API_KEY -e EMAIL_DOMAIN=$EMAIL_DOMAIN symfoni/mailgun-send:latest \
  --to="to@someone.com" \
  --subj="Hey!!" "Just wanted to say hi. \
  --from="me@email.com" \
  --text="Here's the file you wanted; Give me a call!" \
  --html="<html><body>Here is the file; <b>Give me a call!</b></body></html>" \
  --attachment=/path/to/file
```
