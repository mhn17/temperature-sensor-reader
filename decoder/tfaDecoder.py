
class TfaDecoder(object):
    THRESHOLD = 5000
    HIGH_PULSE_COUNT = 43
    LOW_PULSE_COUNT = 14
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
        else:
            if self.state == 'sync':
                if self.pulseCnt == 0:
                    self.pauseCnt += 1
                elif self.pulseCnt >= 13 and self.pulseCnt <= 15:
                    self.frame.append(0)
                    self.frameIndex += 1
                    self.pulseCnt = 0
                elif self.pulseCnt >= 42 and self.pulseCnt <= 44:
                    self.frame.append(1)
                    self.frameIndex += 1
                    self.pulseCnt = 0
                else:
                    self.pulseCnt = 0

                # probably just a noise
                if self.pauseCnt > self.PAUSE_COUNT_MAX:
                    self._reset_values()

                if self.frameIndex == self.FRAME_LENGTH:
                    self._calc_temperature(self.frame[self.TEMPERATURE_SIGNAL_START:self.TEMPERATURE_SIGNAL_END])

    def _reset_values(self):
        self.frame = bytearray()
        self.frameIndex = 0
        self.pulseCnt = 0
        self.pauseCnt = 0
        self.state = 'wait'

    def _calc_temperature(self, temperature_signals):
        print "_calc_temperature"
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
