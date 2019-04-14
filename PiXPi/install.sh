#!/bin/sh
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

###hunk to be injected in /etc/rc.local script
RCLOCAL_SCRIPT="
echo "0" > /sys/class/leds/vocore2\:fuchsia\:status/brightness\n
/bin/ash /root/PiXPi/startup.sh\n
exit 0
"
###inject startup procedure to rc.local if not already contains
echo -e $RCLOCAL_SCRIPT >> /etc/rc.local

###Compile python app to make startup faster
python -m compileall -f $SCRIPTPATH
