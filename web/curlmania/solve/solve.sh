#!/usr/bin/env bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Error: No URL provided."
  echo "Usage: $0 <url>"
  exit 1
fi

# Get the URL from the argument
url="$1"
# Extract the host from the URL (can include port)
host=$(echo "$url" | awk -F/ '{print $3}' | awk -F: '{
  if (NF > 1) {
    print $1 ":" $2
  } else {
    print $1
  }
}')

curl --path-as-is -i -s -k -X $'GET' \
    -H $'Host: '$host -H $'User-Agent: J\'aime la galette saucisse' -H $'LIBEREZ-GCC: OUI' -H $'Content-Type: application/json' -H $'Referer: Je jure solennellement que mes intentions sont mauvaises mais je ne vais pas taper sur l\'infra' -H $'Content-Length: 1337' \
    -b $'jaiplustropdinspi=0' \
    --data-binary $'{\"enbretagne\":                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   \"il fait toujours beau\"}' \
    $url$'/1337?param1=35&param2=0&param3=0' 