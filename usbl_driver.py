#!/usr/bin/python
import sys
sys.path.insert(0, './pynmea2')

import pdb

import time
import pynmea2
import json
import socket
import serial
import math
from decimal import *
from os import system

# destination / output
ip="192.168.2.2"
portnum = 27000
sockitOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sockitOut.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sockitOut.setblocking(False)

#Radius of Earth
R = float(6378137)

# gpsData = {
#     'time_usec' : 0,                        # (uint64_t) Timestamp (micros since boot or Unix epoch)
#     'gps_id' : 0,                           # (uint8_t) ID of the GPS for multiple GPS inputs
#     'ignore_flags' : 56,                    # (uint16_t) Flags indicating which fields to ignore (see GPS_INPUT_IGNORE_FLAGS enum). All other fields must be provided.
#     'time_week_ms' : 0,                     # (uint32_t) GPS time (milliseconds from start of GPS week)
#     'time_week' : 0,                        # (uint16_t) GPS week number
#     'fix_type' : 3,                         # (uint8_t) 0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
#     'lat' : 0,                              # (int32_t) Latitude (WGS84), in degrees * 1E7
#     'lon' : 0,                              # (int32_t) Longitude (WGS84), in degrees * 1E7
#     'alt' : 0,                              # (float) Altitude (AMSL, not WGS84), in m (positive for up)
#     'hdop' : 0,                             # (float) GPS HDOP horizontal dilution of position in m
#     'vdop' : 0,                             # (float) GPS VDOP vertical dilution of position in m
#     'vn' : 0,                               # (float) GPS velocity in m/s in NORTH direction in earth-fixed NED frame
#     've' : 0,                               # (float) GPS velocity in m/s in EAST direction in earth-fixed NED frame
#     'vd' : 0,                               # (float) GPS velocity in m/s in DOWN direction in earth-fixed NED frame
#     'speed_accuracy' : 0,                   # (float) GPS speed accuracy in m/s
#     'horiz_accuracy' : 0,                   # (float) GPS horizontal accuracy in m
#     'vert_accuracy' : 0,                    # (float) GPS vertical accuracy in m
#     'satellites_visible' : 0                # (uint8_t) Number of satellites visible.
# }
#
# rthData = {
#     'ab' : 0,
#     'ac' : 0,
#     'ae' : 0,
#     'sr' : 0,
#     'tb' : 0,
#     'cb' : 0,
#     'te' : 0,
#     'er' : 0,
#     'ep' : 0,
#     'ey' : 0,
#     'ch' : 0,
#     'db' : 0
# }
#
# rovData = {
#     'time_usec' : 0,                        # (uint64_t) Timestamp (micros since boot or Unix epoch)
#     'gps_id' : 0,                           # (uint8_t) ID of the GPS for multiple GPS inputs
#     'ignore_flags' : 56,                    # (uint16_t) Flags indicating which fields to ignore (see GPS_INPUT_IGNORE_FLAGS enum). All other fields must be provided.
#     'time_week_ms' : 0,                     # (uint32_t) GPS time (milliseconds from start of GPS week)
#     'time_week' : 0,                        # (uint16_t) GPS week number
#     'fix_type' : 3,                         # (uint8_t) 0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
#     'lat' : 0,                              # (int32_t) Latitude (WGS84), in degrees * 1E7
#     'lon' : 0,                              # (int32_t) Longitude (WGS84), in degrees * 1E7
#     'alt' : 0,                              # (float) Altitude (AMSL, not WGS84), in m (positive for up)
#     'hdop' : 0,                             # (float) GPS HDOP horizontal dilution of position in m
#     'vdop' : 0,                             # (float) GPS VDOP vertical dilution of position in m
#     'vn' : 0,                               # (float) GPS velocity in m/s in NORTH direction in earth-fixed NED frame
#     've' : 0,                               # (float) GPS velocity in m/s in EAST direction in earth-fixed NED frame
#     'vd' : 0,                               # (float) GPS velocity in m/s in DOWN direction in earth-fixed NED frame
#     'speed_accuracy' : 0,                   # (float) GPS speed accuracy in m/s
#     'horiz_accuracy' : 0,                   # (float) GPS horizontal accuracy in m
#     'vert_accuracy' : 0,                    # (float) GPS vertical accuracy in m
#     'satellites_visible' : 0                # (uint8_t) Number of satellites visible.
# }

sampleRTH = "$USRTH,358.5,1.5,2.8,142.8,52.8,37.2,2.8,-0.6,1.9,178.1,271.9,16*49"
sampleGPS = "$GPGGA,200838.400,3845.0630,N,07727.2770,W,1,06,1.2,111.4,M,-33.4,M,,0000*6A"
# rthData = pynmea2.parse(sampleRTH)
# gpsData = pynmea2.parse(sampleGPS)
# rovData = pynmea2.parse(sampleGPS)

while True:
    #Update Data
    try:
        with open('/dev/ttyUSB0', 'r') as dev:
            streamreader = pynmea2.NMEAStreamReader(dev)
            for msg in streamreader.next():
                rthData = msg
    except:
        print("Failed to read RTH")


    try:
        with open('/dev/ttyACM0', 'r') as dev:
            streamreader = pynmea2.NMEAStreamReader(dev)
            for msg in streamreader.next():
                gpsData = msg
                rovData = msg
    except:
        print("Failed to read RTH")

    #Maths
    #Elevation 0 at horizon?
    hr = rthData.sr * math.cos(rthData.te)

    dn = math.cos(rthData.cb) * hr
    de = math.sin(rthData.cb) * hr

    dLat = dn / R
    #pdb.set_trace()

    dLon = de / (R * math.cos(math.pi) * gpsData.latitude / float(100))

    newLat = gpsData.latitude + dLat * 180 / math.pi
    newLon = gpsData.longitude + dLon * 180 / math.pi

    timestring = (str(gpsData.timestamp)[0:2] + str(gpsData.timestamp)[3:5] + str(gpsData.timestamp)[6:8])
    rovSentence = pynmea2.GGA('GP', 'GGA', (timestring, str(newLat*100), str(gpsData.lat_dir), str(newLon*100), str(gpsData.lon_dir)))
    print(str(gpsData))
    #pdb.set_trace()
    #Send ROV data
    # print("G: " , gpsData)
    # print("R: " , rovData)
    sockitOut.sendto(str(rovSentence), (ip, portnum))
