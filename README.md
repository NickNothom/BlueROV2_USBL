# BlueROV2_USBL

Warning: This project is a WIP, and is highly cuztomized for my application. Its usefullness to others is likely very limited. 


## Setup

Give our location to QGroundControl

socat -u FILE:/dev/ttyACM0,b4800,raw,ignoreeof UDP4-DATAGRAM:192.168.2.1:14401,reuseaddr,ignoreeof

Set up the serial port for the USBL
stty -F /dev/ttyUSB0 115200 -brkint -icrnl -imaxbel -opost -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke
