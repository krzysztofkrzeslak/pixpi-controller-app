#!/bin/sh

APP_PATH="$( cd "$(dirname "$0")" ; pwd -P )"

#set ap name
uci set wireless.ap.ssid=pixpi-`hexdump -C /dev/mtd2 | head -1 | awk '{print $10$11}'`
uci commit

###inject startup procedure to rc.local if not already contains
echo -e "rmmod leds_gpio\n/bin/ash /root/PiXPi/startup.sh \nexit 0" > /etc/rc.local

#compile python app
python -m compileall -f $APP_PATH
