temperature-monitor
===================

Monitor temperature using Digi XBee sensor module



Uses python-xbee
https://code.google.com/p/python-xbee/

<pre>
xbee/
  setup_sensor.py - set the sensor inputs and sleep times
  receiver.py - wait to receive data from temperature sensor 

server/
  read_temp.py - reads temperature, etc from file (written by receiver.py)
  server_temp.py - simple HTTP server that serves the temperature readings
</pre>

