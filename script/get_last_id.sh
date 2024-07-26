#!/bin/bash

psql -h localhost -p 5432 -U safeline-ce -d safeline-ce -t -P footer=off -c \
"SELECT id FROM PUBLIC.MGT_DETECT_LOG_BASIC ORDER BY id desc limit 1" | \
tr -d ' \t\n'