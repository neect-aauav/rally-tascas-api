#!/bin/bash

SKIP_GRANT_TABLES="false"
DEFAULTS="false"
DBNAME="neectrally"
DBNAME_ARG="false"
DBUSER="neect"
DBUSER_ARG="false"
DBPWD=""
DBPWD_ARG="false"
DBHOST="localhost"
DBHOST_ARG="false"
ROOT_PWD=""
SKIP_PROMPTS="false"

show_help() {
	echo "Description: Setup MySQL database to run API."
	echo "Note: This script CAN be run without arguments."
	if [[ $# == 1 ]] ; then
		echo "Issue: $1"
	fi
	echo "Usage: $0 [-d|h|s] [-r|n|u|p <arg>]"
	echo -e " -d:\t use the default values for MySQL database name and user"
	echo -e " -h:\t print this help message"
	echo -e " -s:\t skip installation prompts"
	echo -e " -r:\t set MySQL root password"
	echo -e " -n:\t set MySQL database name"
	echo -e " -u:\t set MySQL user in the format 'user@host'"
	echo -e " -p:\t set MySQL user password"
	exit

}

# handle arguments
while getopts "dhsr:n:u:p:" arg; do
	case $arg in
		d)
			DEFAULTS="true"
			;;
		r) 
			if [[ ${OPTARG:0:1} == "-" ]] || [[ -z $OPTARG ]] ; then
				show_help "Argument -r requires specification of password of MySQL root."
			else
				ROOT_PWD=$OPTARG
			fi
			;;
		n)
			if [[ ${OPTARG:0:1} == "-" ]] || [[ -z $OPTARG ]] ; then
				show_help "Argument -n requires specification of name of MySQL database."
			else
				DBNAME=$OPTARG
				DBNAME_ARG="true"
			fi
			;;
		u)
			if [[ ${OPTARG:0:1} == "-" ]] || [[ -z $OPTARG ]] ; then
				show_help "Argument -u requires specification of MySQL user."
			else
				IN=$OPTARG
				arrIN=(${IN//@/ })
				if [[ ${#arrIN[@]} != 2 ]] ; then
					show_help "Argument -u must take both user and host in the format 'user@host'"
				else
					DBUSER_ARG="true"
					DBHOST_ARG="true"
					DBUSER=${arrIN[0]}
					DBHOST=${arrIN[1]}
				fi
			fi
			;;
		p)
			if [[ ${OPTARG:0:1} == "-" ]] || [[ -z $OPTARG ]] ; then
				show_help "Argument -p requires specification of MySQL user password."
			else
				DBPWD=$OPTARG
				DBPWD_ARG="true"
			fi
			;;
		h)
			show_help
			;;
		s)
			SKIP_PROMPTS="true"
			;;
		*)
			show_help
			;;
	esac
done

# check if mysql is installed
# https://unix.stackexchange.com/a/79631
if [ -f /etc/init.d/mysql* ] ; then
	echo "MySQL present."
else
	install_mysql() {
		if [[ "${SKIP_PROMPTS}" == "true" ]] ; then
			echo "Y" | sudo apt install mysql-server
		else
			sudo apt install mysql-server
		fi

		if [[ "${SKIP_PROMPTS}" == "false" ]] ; then
			read -p "Setup MySQL root password? [Y/n] "
			if [[ $REPLY =~ ^[Yy]$ ]] || [[ $REPLY == '' ]] ; then
				sudo mysql_secure_installation
			fi
		fi

		# skip grant tables to make root use mysql_native_password
		echo ""; echo "Skipping grant tables to make root use 'mysql_native_password'..."
		
		MYCNF=/etc/mysql/my.cnf
		echo "" | sudo tee -a "${MYCNF}" > /dev/null
		echo "[mysqld]" | sudo tee -a "${MYCNF}" > /dev/null
		echo "skip-grant-tables" | sudo tee -a "${MYCNF}" > /dev/null
		sudo systemctl restart mysql
		SKIP_GRANT_TABLES="true"

		QUERY="USE mysql; UPDATE user SET plugin='mysql_native_password' WHERE User='root'; FLUSH PRIVILEGES;"
		echo "Query: $QUERY"
		mysql -e "$QUERY"	
	}
	
	if [[ "${SKIP_PROMPTS}" == "false" ]] ; then
		read -p "MySQL is not installed. Install it now? [Y/n] "
		if [[ $REPLY =~ ^[Yy]$ ]] || [[ $REPLY == '' ]] ; then
			install_mysql
		else
			exit 1
		fi
	else
		install_mysql
	fi
fi

# setup database
if [[ "${DEFAULTS}" == "false" ]] ; then
	if [[ "${DBNAME_ARG}" == "false" ]] ; then
		read -p "Database name($DBNAME): "
		if [ "$REPLY" != '' ] ; then
			DBNAME=$REPLY
		fi
	fi

	if [[ "${DBUSER_ARG}" == "false" ]] ; then
		read -p "User($DBUSER): "
		if [ "$REPLY" != '' ] ; then
			DBUSER=$REPLY
		fi
	fi

	if [[ "${DBPWD_ARG}" == "false" ]] ; then
		read -sp "Password($DBPWD): "
		echo ""
		if [ "$REPLY" != '' ] ; then
			DBPWD=$REPLY
		fi
	fi
	
	if [[ "${DBHOST_ARG}" == "false" ]] ; then
		read -p "Host($DBHOST): "
		if [ "$REPLY" != '' ] ; then
			DBHOST=$REPLY
		fi
	fi
fi

echo ""; echo "Setting up database and user..."

handle_password_print() {
	for ((i=0; i<${#DBPWD}; i++)); do
		echo -n "*"
	done
	echo "'"
}

# check need for root password and run queries
if [ -f /root/.my.cnf ]; then
	if [[ ! -z "`mysql -uroot -proot -sNe "SHOW DATABASES LIKE '${DBNAME}';" 2>/dev/null`" ]] ; then
		echo "[Warning] Already exists a database with the name ${DBNAME}, so it won't be created."
	else
		echo "[Query] CREATE DATABASE ${DBNAME};"
		mysql -e "CREATE DATABASE ${DBNAME};"
	fi
	
	echo -n "[Query] CREATE USER ${DBUSER}@${DBHOST} IDENTIFIED BY '"
	handle_password_print ${DBPWD}
	mysql -e "CREATE USER ${DBUSER}@${DBHOST} IDENTIFIED BY '${DBPWD}'"

	echo "[Query] GRANT ALL PRIVILEGES ON ${DBNAME}.* TO '${DBUSER}'@'${DBHOST}';"
	mysql -e "GRANT ALL PRIVILEGES ON ${DBNAME}.* TO '${DBUSER}'@'${DBHOST}';"

	echo "[Query] FLUSH PRIVILEGES;"
	mysql -e "FLUSH PRIVILEGES;"

else
	if [[ "${ROOT_PWD}" == "" ]] ; then
		echo "Please insert MySQL root password: "
		read -s ROOT_PWD
	fi
	
	if [[ ! -z "`mysql -uroot -proot -sNe "SHOW DATABASES LIKE '${DBNAME}';" 2>/dev/null`" ]] ; then
		echo "[Warning] Already exists a database with the name ${DBNAME}, so it won't be created."
	else
		echo "[Query] CREATE DATABASE ${DBNAME};"
		mysql -uroot -p${ROOT_PWD} -e "CREATE DATABASE ${DBNAME};"
	fi

	echo -n "[Query] CREATE USER ${DBUSER}@${DBHOST} IDENTIFIED BY '"
	handle_password_print ${DBPWD}
	mysql -uroot -p${ROOT_PWD} -e "CREATE USER ${DBUSER}@${DBHOST} IDENTIFIED BY '${DBPWD}'"

	echo "[Query] GRANT ALL PRIVILEGES ON ${DBNAME}.* TO '${DBUSER}'@'${DBHOST}';"
	mysql -uroot -p${ROOT_PWD} -e "GRANT ALL PRIVILEGES ON ${DBNAME}.* TO '${DBUSER}'@'${DBHOST}';"

	echo "[Query] FLUSH PRIVILEGES;"
	mysql -uroot -p${ROOT_PWD} -e "FLUSH PRIVILEGES;"
fi

# create secret.py file
echo ""; echo "Creating secret.py file..."
SECRETS_FILE=neectrally/secrets.py
touch ${SECRETS_FILE}
echo "DB_NAME = '${DBNAME}'" > ${SECRETS_FILE}
echo "DB_USER = '${DBUSER}'" >> ${SECRETS_FILE}
echo "DB_HOST = '${DBHOST}'" >> ${SECRETS_FILE}
echo "DB_PWD = '${DBPWD}'" >> ${SECRETS_FILE}

# remove skip-grant-tables instruction
if [[ "${SKIP_GRANT_TABLES}" == "true" ]]; then
	echo "Removing skip-grant-tables instruction..."
	sudo head -n -3 /etc/mysql/my.cnf > tmp.txt; sudo mv tmp.txt /etc/mysql/my.cnf
	sudo systemctl restart mysql
fi
