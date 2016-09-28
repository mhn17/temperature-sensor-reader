#!/usr/bin/env python

# Sensor Data Reader
# Reads the the data from rtl_fm, decodes the data and writes it to a file

import struct
from decoder.tfaDecoder import TfaDecoder
from reader.rtlReader import RtlReader
from writer.fileWriter import FileWriter

# set constants for reading the data using rtl_fm
BYTE_READ_LENGTH = 1024
RTL_DEVICE = 0
RTL_FREQUENCY = 433.9865
RTL_SAMPLE_RATE = 30

# file for writing the decoded data
FILE_PATH = "./temperature.txt"

# create decoder
decoder = TfaDecoder()

# create reader
reader = RtlReader()
reader.init(RTL_DEVICE, RTL_FREQUENCY, RTL_SAMPLE_RATE)
b = reader.read(BYTE_READ_LENGTH)

# create writer
writer = FileWriter()
writer.init(FILE_PATH)

counter = 0
temperatureSetCounter = 0
# process values
while len(b) == BYTE_READ_LENGTH:
    counter += 1

    # process the read data
    fmt = '' + str(BYTE_READ_LENGTH/2) + 'h'
    values = struct.unpack(fmt, b)
    for value in values:
        decoder.process(value)

    # a new value has been set -> print and write to file
    if temperatureSetCounter < decoder.temperatureSetCounter:
        print "Temperature: " + str(decoder.temperature)
        writer.write(decoder.temperature)
        temperatureSetCounter = decoder.temperatureSetCounter

    # get next data from reader
    b = reader.read(BYTE_READ_LENGTH)
