#!/bin/sh

FG=/Users/barney/.virtualenvs/py2.7/bin/flexget
FLEXGETSERIES=`$FG series list | sed -e '1,3d; $d ;s/^\>//; s/^ //' | sed -e '$d' | sed -e '$d' | cut -f 1-5  -d " "`
sleep 1s
echo $FLEXGERSERIES
IFS=$'\n'
for SERIE in $FLEXGETSERIES
do
    echo "Processing: $SERIE" 
    echo ""   
    $FG series forget $SERIE    
    sleep 1s
done
