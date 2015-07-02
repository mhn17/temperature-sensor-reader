import struct
import unittest
import io
from decoder.tfaDecoder import TfaDecoder

class TfaDecoderTest(unittest.TestCase):
    def setUp(self):
        self.fin = io.open("./../fixtures/rtl_data.dat", mode="rb")
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

        self.assertEqual(26, self.decoder.temperature)