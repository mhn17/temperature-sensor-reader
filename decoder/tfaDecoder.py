from array import array

class TfaDecoder(object):
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
            self.signalIndex = 0