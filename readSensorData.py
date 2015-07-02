from reportlab.graphics.samples.scatter import Scatter

__author__ = 'marc'


import argparse
import sys
import io
import time
import struct
import logging
import numpy as np
import matplotlib.pyplot as plt
from array import array


class decoder(object):
    def __init__(self):
        self.highCounter = 0
        self.foundFrame = 0
        self.frameIndex = 0
        self.signal = array('b')
        self.signalIndex = 0
        self.valueCounter = 0

    def process(self, value):
        self.valueCounter += 1
        if value > 5000:
            self.highCounter += 1
        else:
            self.highCounter = 0

        if self.highCounter == 10:
            self.signal.append(0)
            self.signalIndex += 1
        elif self.highCounter == 34:
            self.signalIndex -= 1
            self.signal[self.signalIndex] = 1
            self.signalIndex += 1

        if self.signalIndex == 47:
            tempSignal = self.signal[20:31]
            tempString = ''
            for value in tempSignal:
                tempString += `value`

            tempInt = int(tempString, 2)
            temp = (1647 - tempInt) / 10
            logging.info('Temperature: %i', temp)
            self.signalIndex = 0


    def plot(self, values):
        intValues = array('i')
        for value in values:
            intValues.append(value)

        a = np.linspace(0,10,100)
        #b = np.exp(-values)
        plt.plot(intValues)
        plt.show()

parser = argparse.ArgumentParser(description='Decoder for weather data of sensors from TFA received with RTL SDR.')
parser.add_argument('--log', type=str, default='WARN', help='Log level: DEBUG|INFO|WARN|ERROR. Default: WARN')
parser.add_argument('inputfile', type=str, nargs=1, help="Input file name. Expects a raw file with signed 16-bit samples in platform default byte order and 30 kHz sample rate. Use '-' to read from stdin. Example: rtl_fm -M -f 868.35M -s 30k | ./decode_elv_wde1.py -")

args = parser.parse_args()

loglevel = args.log
loglevel_num = getattr(logging, loglevel.upper(), None)
if not isinstance(loglevel_num, int):
    raise ValueError('Invalid log level: ' + loglevel)
logging.basicConfig(stream=sys.stdout, level=loglevel_num)
logging.info('starting...')
decoder = decoder()

filename = args.inputfile[0]
if filename == '-':
    filename = sys.stdin.fileno()
fin = io.open(filename, mode="rb")
b = fin.read(1899568)
# values = struct.unpack('1899568h', b)
# decoder.plot(values)

# b = fin.read(512)

while len(b) == 1899568:
    values = struct.unpack('949784h', b)
    for value in values:
        decoder.process(value)

    b = fin.read(1899568)
#
#     #decoder.plot(values)


fin.close()


