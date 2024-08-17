import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import serial

# Some setup 
url = "http://localhost:8086"
token = "CLJ4WNMc9hVFFZOVOQw3bJgCjsqTVN9Ficald4dN9GMd7mWgUf5HoFCGZDm1aHI3AdE4T-Ld3zdCr6t_MNTQNQ=="
org = "BFR DAQ"
client = InfluxDBClient(url=url, token=token, org=org)
bucket = "accelerometer"
write_api = client.write_api(write_options = SYNCHRONOUS)

SERIAL_PORT = '/dev/cu.usbserial-1110'
BAUD_RATE = 9600
ser = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            accel = line.split(',')
            print(accel)
            pointX = Point("acceleration").tag("axis", "X").field("m/s^2", float(accel[0]))
            pointY = Point("acceleration").tag("axis", "Y").field("m/s^2", float(accel[1]))
            pointZ = Point("acceleration").tag("axis", "Z").field("m/s^2", float(accel[2]))
            write_api.write(bucket=bucket, org=org, record=[pointX, pointY, pointZ])
except KeyboardInterrupt:
    print("Writing process stopped.")

finally:
    ser.close()
    client.close()