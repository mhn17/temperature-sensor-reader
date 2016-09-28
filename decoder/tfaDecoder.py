# TfaDecoder
# Decodes data from a TFA Dostman 30.3034.01 wireless temperature sensor
# ----------------------------------------------------------------------
#
# The temperature is decoded in frame with 47 bits. It has the following structure:
# 0000 0001 0110 1010 1011 1011 0111 011 0000 0000 1100 0100
#          |              |             |         |         |
# sync     |id            |temperature  |         |checksum |
#
# Signal encoding:
# see https://www.yumpu.com/en/document/view/377565/wireless-temperature-sensor-decoding-using-arduino
# short:  460 us -> 0
# long:  1435 us -> 1
# pause:  987 us
#
# With a sample rate of 30k this maps to:
# short:	13,80 samples
# long:	    43,05 samples
# pause:	29,61 samples
#
#  The temperature data itself is calculated by:
# 1011 0111 011 -> 1467
# 1024 + 256 + 128 + 32 + 16 + 8 + 2 + 1 = 1467
#
# Subtract the value from 1647 and device by 10:
# 1647 - 1467 = 180
# 180 / 10 = 18.0

class TfaDecoder(object):
    THRESHOLD = 5000
    HIGH_PULSE_COUNT_MIN = 42
    HIGH_PULSE_COUNT_MAX = 44
    LOW_PULSE_COUNT_MIN = 13
    LOW_PULSE_COUNT_MAX = 15
    PAUSE_COUNT_MIN = 29
    PAUSE_COUNT_MAX = 32
    FRAME_LENGTH = 47
    TEMPERATURE_SIGNAL_START = 20
    TEMPERATURE_SIGNAL_END = 31

    def __init__(self):
        self.temperature = None
        self.temperatureSetCounter = 0

        self.pulseCnt = 0
        self.pauseCnt = 0
        self.frame = None
        self.frameIndex = None
        self.state = 'wait'

        self._reset_values()

    def process(self, value):
        value = abs(value)
        if value > self.THRESHOLD:
            self._analyse_high_sample(value)
        else:
            if self.state == 'sync':
                if self.pulseCnt == 0:
                    # count pause samples
                    self.pauseCnt += 1
                elif self.pulseCnt >= self.LOW_PULSE_COUNT_MIN and self.pulseCnt <= self.LOW_PULSE_COUNT_MAX:
                    # low pulse detected, add a 0 to the frame
                    self.frame.append(0)
                    self.frameIndex += 1
                    self.pulseCnt = 0
                elif self.pulseCnt >= self.HIGH_PULSE_COUNT_MIN and self.pulseCnt <= self.HIGH_PULSE_COUNT_MAX:
                    # high pulse detected, add a 1 to the frame
                    self.frame.append(1)
                    self.frameIndex += 1
                    self.pulseCnt = 0
                else:
                    # reset pulse count
                    self.pulseCnt = 0

                # probably just a noise
                if self.pauseCnt > self.PAUSE_COUNT_MAX:
                    self._reset_values()

                # frame fully detected => calculate the temperature
                if self.frameIndex == self.FRAME_LENGTH:
                    self._calc_temperature(self.frame[self.TEMPERATURE_SIGNAL_START:self.TEMPERATURE_SIGNAL_END])

    def _reset_values(self):
        self.frame = bytearray()
        self.frameIndex = 0
        self.pulseCnt = 0
        self.pauseCnt = 0
        self.state = 'wait'

    def _analyse_high_sample(self, value):
        # the pause between two pulses needs to be between 29 and 32
        if self.state == 'sync' and self.pulseCnt == 0:
            if self.pauseCnt < self.PAUSE_COUNT_MIN or self.pauseCnt > self.PAUSE_COUNT_MAX:
                self._reset_values()

        # add previous sample to pulse count because it starts with a low
        if self.pulseCnt == 0:
            self.pulseCnt += 1
            self.pauseCnt = 0

        self.pulseCnt += 1
        self.state = 'sync'

    def _calc_temperature(self, temperature_signals):
        coded_temperature = self._calc_int_value_of_coded_temperature(temperature_signals)
        self.temperature = (1647 - float(coded_temperature)) / 10
        self.temperatureSetCounter += 1
        self._reset_values()

    @staticmethod
    def _calc_int_value_of_coded_temperature(temperature_signals):
        coded_temperature_string = ''
        for value in temperature_signals:
            coded_temperature_string += `value`
        return int(coded_temperature_string, 2)
