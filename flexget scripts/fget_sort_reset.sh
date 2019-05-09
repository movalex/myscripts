#!/bin/sh

log_file="$HOME/logs/sort.log"
exec 1>> $log_file 2>/dev/null 

TRM=/usr/local/bin/transmission-remote
FG=/usr/local/bin/flexget
SERVER="9091 --auth admin:iddqd456456"
TORRENTLIST=`$TRM $SERVER --list | sed -e '1d;$d;s/*//' | awk '{print $1}'`
D=$(date)
SORTER=false
SEEDING=0
UNCOMPLETED=0
LOCATION="/Volumes/HARD1/TVTEMP"
SIZE=$(du -s $LOCATION | awk '{print $1}')

echo `seq -f "-" -s '' ${#D}`
echo $D
echo `seq -f "-" -s '' ${#D}`

$TRM $SERVER --list | sed -e '1d;$d;s/*//'

if ! [[ $TORRENTLIST ]];  then
    echo "Torrent list is empty"
    if [[ $SIZE -gt 600000 ]];  then
        echo "setting sort to True"
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
            STATE_IDLE=` $INFO|grep "State: Idle" `
            STATE_SEEDING=` $INFO|grep "State: Seeding" `

            if [[ "$STATE_STOPPED" ]]; then
                 echo "trying to restart torrent"
                 $TRM $SERVER --torrent $TORRENTID -s
                 if [[ "$NODATA_ERROR" ]]; then
                     echo "Restart failed. Cleaning fault torrent"
                     $TRM $SERVER --torrent $TORRENTID --remove
                 fi 
            fi

            if [[ "$STATE_LOCATION" ]]; then
                if [[ "$STATE_FINISHED" ]];  then
                    echo "Torrent #$TORRENTID (`$INFO |grep "Name" | sed -e 's/^ \{1,\}//g; s/Name: //g'`) is finished"
                    echo "Removing torrent from list"
                    $TRM $SERVER --torrent $TORRENTID --remove
                    echo "Torrent #$TORRENTID has been removed" 
                    SORTER=true
                elif [[ "$DL_COMPLETED" ]] && [[ ( "$STATE_SEEDING" || "$STATE_IDLE" ) ]]; then
                SEEDING=$(( SEEDING + 1 ))
                elif ! [[ "$DL_COMPLETED" ]];  then
                    echo "Torrent #$TORRENTID is not completed. Ignoring."
                    UNCOMPLETED=$(( UNCOMPLETED + 1 ))
                fi
            elif ! [[ $STATE_LOCATION ]]; then
                if [[ "$STATE_FINISHED" ]];  then
                    echo $STATE_FINISHED
                    echo "Cleaning finished transmission items"
                    $TRM $SERVER --torrent $TORRENTID --remove
                elif ! [[ "$DL_COMPLETED" ]];  then
                    echo "Torrent #$TORRENTID is not completed, ignoring. But who cares."
                elif [[ ( "$STATE_SEEDING" || "$STATE_IDLE" ) ]]; then
                    echo "torrent is seeding"
                else echo "another unexpected condition, passing"
                fi
            fi
        done
fi

if [[ $UNCOMPLETED -eq 0 ]];  then
    :
elif [[ $UNCOMPLETED -eq 1 ]];  then
    echo "There's one torrent still downloading"
else
    echo "There's $UNCOMPLETED torrents still downloading"
fi

if [[ $SEEDING -eq 0 ]];  then
    :
elif [[ $SEEDING -eq 1 ]];  then
    echo "There's one torrent currently seeding"
else
    echo "There's $SEEDING torrents currently seeding"
fi

if [[ $SORTER = true ]] && [[ $UNCOMPLETED -eq 0 ]] && [[ $SEEDING -eq 0 ]];  then
    echo "sorting things out"
    $FG execute --tasks sort
else
    :
fi 
