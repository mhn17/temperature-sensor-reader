Temperature Sensor Reader
=========================

Description
-----------
The Temperature Sensor Reader listens for data send from a wireless temperature sensor, decodes it and writes the value to a file. It uses [RTL SDR](http://sdr.osmocom.org/trac/wiki/rtl-sdr "RTL SDR") to receive the data.

Dependencies
------------
- Python 2.7
- [RTL SDR](http://sdr.osmocom.org/trac/wiki/rtl-sdr "RTL SDR")
- TFA Dostman 30.3034.01 wireless temperature sensor

Run application
---------------

    python readSensorData.py
