SERVICE="deluged"
if pgrep -f "$SERVICE" &> /dev/null; then 
        echo "Deluge is running, starting VPN"
        #scutil --nc start "VPN Unlimited (Luxembourg, IPSec)" && sleep 3s
        source /Users/barney/.profile 
        uvpn start
        echo "Starting..."
        sleep 5
        echo "Done"
    else 
        echo "Deluge not running"
        sh /Users/barney/.config/deluge/deluge_autorun.sh  && sleep 2s
        echo "Deluge started, now starting VPN"
        #scutil --nc start "VPN Unlimited (Luxembourg, IPSec)" && sleep 5s
        source /Users/barney/.profile 
        echo "Starting..."
        uvpn start
        sleep 5
        echo "Done"
    fi

