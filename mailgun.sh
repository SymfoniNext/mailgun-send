#!/bin/bash

function usage() {
  echo "Usage:"
  echo "./mailgun.sh <consul-addr> <key-name> <to> <subject> <message> <from>"
  echo "./mailgun.sh localhost:8500 mailgun \"You <you@you.com>\" \"subject\" \" \"hey you!\" \"Me <me@me.com>\""
  exit 1
}

consul=$1
if [[ -z "$consul" ]]; then
  usage;
fi

shift
keyname=$1
if [[ -z "$keyname" ]]; then
  usage;
fi

shift
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

# Get something from consul
declare -A config
for v in $(curl -s "http://$consul/v1/kv/$keyname?recurse=1" | jq -r "map(\"\(.Key):\(.Value)\") | .[] | ltrimstr(\"$keyname/\")"); do
  config[${v%:*}]=$(base64 -d < <(echo "${v#*:}"))
done


curl -v --user "api:${config['api_key']}" https://api.mailgun.net/v3/${config['email_domain']}/messages \
  -F from="${from}" \
  -F to="${to}" \
  -F subject="${subj}" \
  -F text="${message}" 
