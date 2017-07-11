#!/usr/bin/env bash

export GDELT_HISTORIC_FILE_PATH='/Users/panchicore/www/es-gdelt/data/old/*.CSV'
export GDELT_REALTIME_FILE_PATH='/Users/panchicore/www/es-gdelt/data/realtime/*.CSV'
export ES_HOST=http://localhost:9200/
export ES_USER=elastic
export ES_PASSWORD=changeme
export ES_GDELT_INDEX=gdelt
export SLACK_NOTIFICATIONS_ENABLED=1
export SLACK_NOTIFICATIONS_URL=https://hooks.slack.com/services/XXXX/YYYYY/ZZZZZ