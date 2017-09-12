#!/bin/bash

function usage() {
  echo "Usage:"
  echo "export API_KEY=xxx EMAIL_DOMAIN=xxx"
  echo "./mailgun.sh <to> <subject> <message> <from>"
  echo "./mailgun.sh \"You <you@you.com>\" \"subject\" \" \"hey you!\" \"Me <me@me.com>\""
  exit 1
}

if [[ -z "${API_KEY}" ]]; then
  usage;
fi

if [[ -z "${EMAIL_DOMAIN}" ]]; then
  usage;
fi

to=$1
if [[ -z "$to" ]]; then
  usage;
fi

shift
subj=$1
if [[ -z "$subj" ]]; then
  usage;
fi

shift
message=$1
if [[ -z "$message" ]]; then
  usage;
fi

shift
from=$1
if [[ -z "$from" ]]; then
  usage;
fi


curl -f -v --user "api:${API_KEY}" https://api.mailgun.net/v3/${EMAIL_DOMAIN}/messages \
  -F from="${from}" \
  -F to="${to}" \
  -F subject="${subj}" \
  -F text="${message}" 
