stty -F /dev/ttyUSB0 115200 -brkint -icrnl -imaxbel -opost -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke

screen -dm -S gpsToQGC socat -u FILE:/dev/ttyACM0,b4800,raw,ignoreeof UDP4-DATAGRAM:192.168.2.1:14401,reuseaddr,ignoreeof