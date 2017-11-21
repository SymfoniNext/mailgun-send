#!/usr/bin/env python3

import argparse, sys, os, requests

if not "API_KEY" in os.environ:
    print("API_KEY is missing from the environment")
    sys.exit(4)
API_KEY = os.environ["API_KEY"]
if not "EMAIL_DOMAIN" in os.environ:
    print("EMAIL_DOMAIN is missing from the environment")
    sys.exit(4)
EMAIL_DOMAIN = os.environ["EMAIL_DOMAIN"]


parser = argparse.ArgumentParser(description='Send emails via mailgun')
parser.add_argument("--to", action="append", help="Who to send email to", required=True)
parser.add_argument("--cc", action="append", help="Who to cc email to", default=[])
parser.add_argument("--bcc", action="append", help="Who to bcc email to", default=[])
parser.add_argument("--from", help="Who the email is from")
parser.add_argument("--subj", help="Subject of your email", required=True)
parser.add_argument("--text", help="Text version of your message")
parser.add_argument("--html", help="HTML version of your message")
parser.add_argument("--html-file", help="HTML version of your message from file")
parser.add_argument("--inline", action="append", help="Attachments to include inline", default=[])
parser.add_argument("--attachment", action="append", help="Attachments to include", default=[])
parser.add_argument("--tag", action="append", help="Tags for the email", default=[])

args = parser.parse_args()

if args.html_file:
    try:
        with open(args.html_file, "rb") as f:
            args.html = f.readlines()
    except:
        print("%s: no such file" % args.html_file)
        sys.exit(5)

if args.html is None and args.text is None:
    print("Missing --text or --html[-file]")
    sys.exit(6)


def get_files(args):
    def get(name, filepath):
        try:
            with open(filepath, "rb") as f:
                return (name, (os.path.basename(filepath), f.read()))
        except:
            print("%s: %s file not found" % (filepath, name))
            sys.exit(55)

    files = []
    for f in args.attachment:
        files.append(get("attachment", f))
    for f in args.inline:
        files.append(get("inline", f))

    return files

def get_payload(args):
    data={
        "to": args.to,
        "subject": args.subj
        }
    if vars(args)["from"] is None:
        data["from"] = "no-reply@%s" % EMAIL_DOMAIN
    else:
        data["from"] = vars(args)["from"] 
    if args.cc:
        data["cc"] = args.cc
    if args.bcc:
        data["bcc"] = args.bcc
    if args.text:
        data["text"] = args.text
    if args.html:
        data["html"] = args.html
    if args.tag:
        data["o:tag"] = args.tag

    return data

r = requests.post(
        "https://api.mailgun.net/v3/%s/messages" % EMAIL_DOMAIN,
        auth=("api", API_KEY),
        files=get_files(args),
        data=get_payload(args)
       )

if r.status_code is not 200:
    print("Status code: %s" % r.status_code)
    sys.exit(10)
