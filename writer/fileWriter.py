# FileWriter
# Writes the temperature data to a file

class FileWriter(object):
    def __init__(self):
        self.file = None
        self.path = "./output.txt"

    def init(self, path):
        self.path = path

    def write(self, temperature):
        self.file = open(self.path, "w")
        self.file.write("temperature: {}".format(temperature))
        self.file.close()
