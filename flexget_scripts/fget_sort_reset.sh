#!/bin/sh

log_file="$HOME/logs/sort.log"
# exec 1>> $log_file 2>/dev/null 

TRM=/usr/local/bin/transmission-remote
FG=/usr/local/bin/flexget
SERVER="9091 --auth admin:password"
TORRENTLIST=`$TRM $SERVER --list | sed -e '1d;$d;s/*//' | awk '{print $1}'`
D=$(date)
SORTER=false
SEEDING=0
LOCATION="/Volumes/Elements/TVTEMP"
SORT_FOLDER="/Volumes/Elements/SORT"

if [ ! -d $LOCATION ]; then
    echo "TVTEMP folder not found"
    mkdir $LOCATION 
fi
if [ ! -d $SORT_FOLDER ]; then
    echo "SORT folder not found"
    mkdir $SORT_FOLDER
fi

SIZE=$(du -s $LOCATION | awk '{print $1}')

echo `seq -f "-" -s '' ${#D}`
echo $D
echo `seq -f "-" -s '' ${#D}`

$TRM $SERVER --list | sed -e '1d;$d;s/*//'

if ! [[ $TORRENTLIST ]];  then
    echo "Torrent list is empty"
    if [[ $SIZE -gt 600000 ]];  then
        SORTER=true
    fi
else
    for TORRENTID in $TORRENTLIST
        do
            echo Processing: $TORRENTID
            INFO=`echo $TRM $SERVER --torrent $TORRENTID --info` 
            NODATA_ERROR=` $INFO|grep "Error: No data found!" `
            DL_COMPLETED=` $INFO|grep "Percent Done: 100%" `
            STATE_LOCATION=` $INFO|grep "Location: $LOCATION" `
            STATE_STOPPED=` $INFO|grep "State: Stopped" `
            STATE_FINISHED=` $INFO|grep "State: Finished" `

            if [[ "$STATE_STOPPED" ]]; then
                 echo "trying to restart torrent"
                 $TRM $SERVER --torrent $TORRENTID -s
                 if [[ "$NODATA_ERROR" ]]; then
                     echo "Restart failed. Cleaning fault torrent"
                     $TRM $SERVER --torrent $TORRENTID --remove
                 fi 
            fi

            echo $STATE_LOCATION
            
            if [[ "$STATE_LOCATION" ]]; then
                if [[ "$DL_COMPLETED" ]];  then
                    echo "Torrent #$TORRENTID (`$INFO |grep "Name" | sed -e 's/^ \{1,\}//g; s/Name: //g'`) is finished"
                    $TRM $SERVER --torrent $TORRENTID --move "$SORT_FOLDER" 
                    $TRM $SERVER --torrent $TORRENTID --remove
                fi
            fi
        done
        SORTER=true
fi


if [[ $SORTER = true ]];  then
    echo "sorting things out"
    $FG execute --tasks sort
fi 

