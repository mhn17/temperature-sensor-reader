import subprocess

# RtlReader
# Opens rtl_fm as a subprocess and reads the data
class RtlReader(object):
    def __init__(self):
        self.sdr = None

    def init(self, device_id, frequency, sampleRate):
        self.sdr = subprocess.Popen("rtl_fm -d " + str(device_id) + " -f " + str(frequency) + "M -M am -s " + str(sampleRate) + "k",
                                    stdout=subprocess.PIPE,
                                    stderr=open('error.txt', 'a'),
                                    shell=True)

    def read(self, length):
        return self.sdr.stdout.read(length)
