#!/bin/sh

FGET=/usr/local/bin/flexget
D=$(date)
echo "$D - `$FGET seen forget rt`" >> /Users/barney/logs/tv1_seen.log
