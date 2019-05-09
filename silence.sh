sudo nvram SystemAudioVolume="%00" # does nothing
osascript -e 'set volume with output muted'
echo "run at $(date)" >> /var/log/silence_log.txt
