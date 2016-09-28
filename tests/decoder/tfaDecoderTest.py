import struct
import unittest
import io
import os

import decoder
from decoder.tfaDecoder import TfaDecoder

# run with "python -m unittest tests.decoder.tfaDecoderTest" from root directory
class TfaDecoderTest(unittest.TestCase):
    def setUp(self):
        self.fin = io.open(os.path.dirname(__file__) + "/../fixtures/rtl_sampleData.dat", mode="rb")
        self.decoder = TfaDecoder()

    def tearDown(self):
        self.fin.close()

    def testTemperature(self):
        b = self.fin.read(1024)
        while len(b) == 1024:
            values = struct.unpack('512h', b)
            for value in values:
                self.decoder.process(value)

            b = self.fin.read(1024)

        self.assertEqual(19.6, self.decoder.temperature)
