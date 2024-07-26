#!/bin/bash

# shellcheck disable=SC1090
source "$1"logger.sh

last_id=$2

# 判断是否有上次 ID 参数
if [ -z "$last_id" ]; then
  error "没有传递上次 ID 参数"
fi

psql -h localhost -p 5432 -U safeline-ce -d safeline-ce -t -P footer=off -c \
"
SELECT timestamp, CONCAT(PROVINCE, CITY) AS SRC_CITY, SRC_IP, CONCAT(HOST, ':', DST_PORT) AS HOST, url_path, rule_id, id FROM PUBLIC.MGT_DETECT_LOG_BASIC where id > '$last_id' ORDER BY id
" | \
tr -d ''