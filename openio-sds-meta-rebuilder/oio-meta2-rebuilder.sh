#!/bin/bash
#set -x
usage() {
	echo "Usage: `basename $0` -r ip_redis_host:redis_port -n namespace"
	echo "Example: `basename $0` -r 192.120.17.12:6051 -n OPENIO " ;
	exit
}

[ $# -ne 4 ] && usage


while getopts ":r:n:" opt; do
  case $opt in
    r)
      echo "-r was triggered, Parameter: $OPTARG" >&2
      REDIS_HOST=${OPTARG/:*/}
      REDIS_PORT=${OPTARG/*:/}
      if [[ $REDIS_HOST == "" ]]
          then
          echo "Missing  ip_redis_host"
	  exit 1
      fi
      if [[ $REDIS_PORT == "" ]]
	  then
	      echo "Missing  redis_port"
	      exit 1
      fi
      ;;
    n)
      echo "-n was triggered, Parameter: $OPTARG" >&2
      NAMESPACE=$OPTARG
      ;;
     *)
	usage
	exit 0
      ;;
  esac
done


#Get account list
redis_bin=$(which redis-cli)
ACCOUNT_LIST=$(redis-cli -h $REDIS_HOST -p $REDIS_PORT  keys account:* | sed 's@.*account:\(.*\)@\1@' | tr "\n" " ")

#Launch meta1 repair
for account in $ACCOUNT_LIST
do
	openio container list --oio-ns ${NAMESPACE} --oio-account $account -f value -c Name --full \
	| while read REF
	do
	    echo "openio container set $REF --property sys.last_rebuild=$(date +%s) --oio-ns ${NAMESPACE} --oio-account $account"
	done
done
