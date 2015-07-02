import argparse
import sys
import io
import struct
from decoder.tfaDecoder import TfaDecoder

BYTE_READ_LENGTH = 1025

# parse arguments
# python readSensorData path/to/file
parser = argparse.ArgumentParser(description='Decoder for weather data of sensors from TFA received with RTL SDR.')
parser.add_argument('inputfile', type=str, nargs=1, help="Input file name. Expects a raw file with signed 16-bit samples in platform default byte order and 24 kHz sample rate.")
args = parser.parse_args()

# create decoder
decoder = TfaDecoder()

# read file
filename = args.inputfile[0]
if filename == '-':
    filename = sys.stdin.fileno()
fin = io.open(filename, mode="rb")

# read first bytes
b = fin.read(BYTE_READ_LENGTH)

counter = 0
# process values
while len(b) == BYTE_READ_LENGTH:
    counter += 1

    fmt = '' + str(BYTE_READ_LENGTH/2) + 'h'
    values = struct.unpack(fmt, b)
    for value in values:
        decoder.process(value)

    b = fin.read(BYTE_READ_LENGTH)

# close file
fin.close()


