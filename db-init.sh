#!/bin/bash

RED='\033[0;31m'
if [ ! -f app/php/secret.php ]; then
    echo -e "${RED}Missing file 'secret.php'"
    echo -e "${RED}Press Ctrl + C to close and create secret as follows:"
    echo -e "${RED}\t$ sudo chmod +x secret.sh"
    echo -e "${RED}\t$ ./secret.sh"
    exit
fi

SERVER="localhost:80"
if [ ! -z "$1" ]; then
    SERVER=$1
fi

until $(curl --output /dev/null --silent --head --fail -sX GET $SERVER/php/setup-db); do
    echo "Trying $SERVER..."
    sleep 3
done

echo "Database is ready"
echo "Server running on http://$SERVER"