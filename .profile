alias src='source ~/.profile'

export LC_ALL=en_US.UTF-8  
export LANG=en_US.UTF-8

export PS1="\[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]\$ "
export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad
alias ls='ls -GFh'

alias poweroff='sudo /sbin/shutdown -h now'
alias sleepy='~/sandbox/sleepy-mac.py'

alias db='cd ~/Dropbox/DOCUMENTS'
alias py3='source ~/.virtualenvs/py3/bin/activate' 
alias py2='source ~/.virtualenvs/py2.7/bin/activate' 
alias tw='py3 && rainbowstream'
alias bp='py3 && bpython'

# fan control
alias smc="/Applications/smcFanControl.app/Contents/Resources/smc"

function _fan() {
    RPM=$1
    smc -k F0Mn -w `printf '%x\n' $(expr $RPM \* 4)` 
}
alias fan="_fan"

# theFuck
alias fuck='$(thefuck $(fc -ln -1))'
# You can use whatever you want as an alias, like for mondays:
alias FUCK='fuck'

alias ose='open /Applications/Utilities/Script\ Editor.app/'
alias slog="tail -f -n 200 /var/log/system.log"

export OSA='osascript -e'
export FNDR='"Finder"'
export SE='"Script Editor"'
alias trash='$OSA "tell app $FNDR to empty"'
alias CSE='$OSA "tell app $SE to quit"'

# top
alias cpu='top -o cpu'
alias mem='top -o rsize' # memory

# meduza
alias mm='meduza --sort oldest'
alias mmc='meduza --exchange'

#flexget
function _fget() {
    flexget execute --tasks $1 $2;
}
alias fget="_fget"

alias htop='sudo htop'
# transmission
alias trm-start='brew services start transmission'
alias trm-stop='brew services stop transmission'
alias trm='transmission-remote -n admin:iddqd456456'
alias trm-id='trm -l | grep -v 'ID' | sort -n -k 2'
alias trm-active='trm -l | grep -v 'Stopped'| grep -v 'Idle' | sort -n'
alias trm-idle='trm -l | grep 'Idle'| sort  -n -k 2'

# weather
alias wttr='curl -4 wttr.in/Moscow'
alias cal="gcal --starting-day=1"

# autocomplete commands with sudo 
complete -cf sudo

# functions
function _flog() {
    tail -n $1 -f /var/log/fail2ban.log;
}
alias flog="_flog"

function _vol() { 
    osascript -e "set Volume $1"; 
    }
alias vl='_vol'

function _uvpn() {
   scutil --nc $1 "VPN Unlimited (Croatia, IPSec)" 
}
alias uvpn="_uvpn" #use `uvpn start | uvpn stop` 

export PATH="/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin:/usr/local/sbin:$PATH"

export EDITOR="/usr/bin/vim"


#skip by word key bindings

bind '"\eOD": backward-word'
bind '"\eOC": forward-word'

# thefuck
eval $(thefuck --alias)

#docker
export DOCKER_TLS_VERIFY="1" export DOCKER_HOST="tcp://192.168.99.100:2376" export DOCKER_CERT_PATH="/Users/barney/.docker/machine/machines/default" export DOCKER_MACHINE_NAME="default" # Run this command to configure your shell: # eval $(docker-machine env default)
export PATH="/usr/local/opt/gettext/bin:$PATH"
#deluge
alias deluge-console="/Applications/Deluge.app/Contents/MacOS/deluge-console"
