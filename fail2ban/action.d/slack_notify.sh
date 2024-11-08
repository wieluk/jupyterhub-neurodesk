#!/bin/bash
# Version 1.0
# Send Fail2ban notifications using a Slack Webhook

function talkToSlack() {
    message=$1
    payload="payload={\"text\": \"${message}\"}"
    curl -s -X POST --data-urlencode "${payload}" ${SLACK_WEBHOOK_URL} > /dev/null 2>&1
}

if [ -z "$SLACK_WEBHOOK_URL" ]; then
    echo "SLACK_WEBHOOK_URL environment variable is not set"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage $0 -a ( start || stop ) || -b $IP || -u $IP || -r $REASON"
    exit 1
fi

while getopts "a:b:u:r:" opt; do
    case "$opt" in
        a)
            action=$OPTARG
        ;;
        b)
            ban=y
            ip_add_ban=$OPTARG
        ;;
        u)
            unban=y
            ip_add_unban=$OPTARG
        ;;
        r)
            reason=$OPTARG
        ;;
        ?)
            echo "Invalid option. -$OPTARG"
            exit 1
        ;;
    esac
done

if [[ ! -z ${action} ]]; then
    case "${action}" in
        start)
            talkToSlack "Fail2ban has been started"
        ;;
        stop)
            talkToSlack "Fail2ban has been stopped"
        ;;
        *)
            echo "Incorrect option"
            exit 1
        ;;
    esac
elif [[ ${ban} == "y" ]]; then
    talkToSlack "The IP ${ip_add_ban} has been banned due to ${reason}. https://ipinfo.io/${ip_add_ban}"
    exit 0
elif [[ ${unban} == "y" ]]; then
    talkToSlack "The IP: ${ip_add_unban} has been unbanned."
    exit 0
else
    echo "Invalid or missing arguments"
    exit 1
fi
