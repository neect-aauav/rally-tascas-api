#!/bin/bash

if [ ! -f db-config.json ] ; then
    echo "Missing configuration file 'db-config.json'"
    exit
fi

fetch_json () {
    formatted_key="\"$1\""
    local result=$(grep -o ''$formatted_key': "[^"]*' db-config.json | grep -o '[^"]*$')
    echo $result
}

HOST=$(fetch_json host)
USERNAME=$(fetch_json username)
PASSWORD=$(fetch_json password)
NAME="rallyneect"

echo "Creating secret.php file..."

SECRET_FILE=app/php/secret.php
touch ${SECRET_FILE}

echo "<?php" > ${SECRET_FILE}
echo "\$db_host='$HOST';" >> ${SECRET_FILE}
echo "\$db_username='$USERNAME';" >> ${SECRET_FILE}
echo "\$db_password='$PASSWORD';" >> ${SECRET_FILE}
echo "\$db_name='$NAME';" >> ${SECRET_FILE}