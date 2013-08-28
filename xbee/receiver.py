"""
Wait for XBee sensor readings to come in and save them to
a CSV file.
"""

import serial
import struct
import csv
from xbee import ZigBee
from pprint import pprint
from datetime import datetime

ser = serial.Serial('/dev/ttyUSB0')

xb = ZigBee(ser)

def dump_power_level():
    xb.at(command='DB')
    r = xb.wait_read_frame()
    if r and r.get('command') == 'DB':
        strength = struct.unpack('>B',r['parameter'])[0]
        print 'signal strength = ',strength,hex(strength)


def handle_adc_data(r, timestamp, datawriter):
    raw_light = r['samples'][0]['adc-1']
    raw_temp = r['samples'][0]['adc-2']
    raw_hum = r['samples'][0]['adc-3']
      
    light_mv = 1200*raw_light/1023.0
    temp_mv = 1200*raw_temp/1023.0
    hum_mv = 1200*raw_hum/1023.0

    temp_C = (temp_mv - 500.0)/10.0
    temp_F = temp_C*9/5.0 + 32.0

    hum_rh = ((hum_mv*108.2/33.2)/5000 - 0.16)/0.0062
    date = datetime.isoformat(timestamp)
    #print 'Timestamp, Temp(F), RH h(%), light', date , temp_F, hum_rh, light_mv
    print date, temp_F, hum_rh, light_mv
    #print >>data_file, date, temp_F, hum_rh, light_mv
    datawriter.writerow( (date, temp_F, hum_rh, light_mv) )

    current_f = open('current_temp.dat', 'w')
    print >>current_f, '#Timestamp, Temp(F), RH h(%), light'
    print >>current_f, date, temp_F, hum_rh, light_mv
    current_f.close()


# Only keep one sample when the sensor wakes up
min_sample_duration = 30  # seconds
#min_sample_duration = 2  # seconds - short for testing
prev_timestamp = datetime.now()

# When the sensor wakes up, ask for the battery voltage periodically
voltage_duration = 3600 # seconds
prev_voltage_timestamp = datetime.now()


data_file = open('temperature.dat', 'w', 0)
datawriter = csv.writer(data_file, delimiter= ' ')

print '# Timestamp, Temperature(F), Relative Humidity (%), light (arbitrary)'
datawriter.writerow( ('# Timestamp','Temperature(F)', 'Relative Humidity (%)', 'light (arbitrary)') )

voltage_file = open('voltage.dat','w', 0)
print >>voltage_file, '# Timestamp, Battery Voltage'

while 1:
    r = xb.wait_read_frame()
    #pprint(r)
    if r['id'] == 'rx_io_data_long_addr':
        timestamp = datetime.now()
        delta = timestamp - prev_timestamp
        if delta.total_seconds() > min_sample_duration:
            handle_adc_data(r, timestamp, datawriter)
            data_file.flush()
            #print 'delta = ',delta.total_seconds()
            prev_timestamp = timestamp
            dump_power_level()

        voltage_delta = timestamp - prev_voltage_timestamp
        if voltage_delta.total_seconds() > voltage_duration:
            # quick sent a check on the battery voltage
            xb.remote_at(command='%V', frame_id=b'\x01')
            r = xb.wait_read_frame()
            if r['id'] == 'remote_at_response':
                data = struct.unpack('> H',r['parameter'])[0]
                voltage = data/1024.0
                print >>voltage_file, timestamp,', ', voltage
                voltage_file.flush()
                prev_voltage_timestamp = timestamp

