
class TfaDecoder(object):
    THRESHOLD = 5000
    HIGH_COUNT_HIGH = 30
    HIGH_COUNT_LOW = 8
    FRAME_LENGTH = 47
    TEMPERATURE_SIGNAL_START = 20
    TEMPERATURE_SIGNAL_END = 31

    def __init__(self):
        self.temperature = None
        self.temperatureSetCounter = 0
        self.highCounter = 0
        self.signals = None
        self.signalsIndex = None

        self._reset_values()

    def process(self, value):
        if value > self.THRESHOLD:
            self.highCounter += 1
        else:
            if self.highCounter > 0:
                self._analyze_high_counts(self.highCounter)

            self.highCounter = 0

    def _reset_values(self):
        self.signals = bytearray()
        self.signalsIndex = 0

    def _analyze_high_counts(self, high_counts):
        # if the high counts is higher than the low threshold, add a new signal set to 0
        if high_counts > self.HIGH_COUNT_LOW:
            self.signals.append(0)
            self.signalsIndex += 1

        # if the high counts is also higher than the high threshold, replace new signal value with 1
        if high_counts > self.HIGH_COUNT_HIGH:
            self.signalsIndex -= 1
            self.signals[self.signalsIndex] = 1
            self.signalsIndex += 1

        # if end of frame, calculate the temperature
        if self.signalsIndex == self.FRAME_LENGTH:
            self._calc_temperature(self.signals[self.TEMPERATURE_SIGNAL_START:self.TEMPERATURE_SIGNAL_END])

    def _calc_temperature(self, temperature_signals):
        coded_temperature = self._calc_int_value_of_coded_temperature(temperature_signals)
        self.temperature = (1647 - coded_temperature) / 10
        self.temperatureSetCounter += 1
        self._reset_values()

    @staticmethod
    def _calc_int_value_of_coded_temperature(temperature_signals):
        coded_temperature_string = ''
        for value in temperature_signals:
            coded_temperature_string += `value`
        return int(coded_temperature_string, 2)
