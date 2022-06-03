import numpy

from ru.rks.meteo.Assist.MeteoAssist import CHANNEL_COUNT
from ru.rks.meteo.hrit.body.tag.HritSubTagRadiometricProcessing import HritSubTagRadiometricProcessing


class HritTagRadiometricProcessing:

    def __init__(self):
        self.radiometrics = []

    @staticmethod
    def convertFromUfd(radiometrics):
        res = HritTagRadiometricProcessing()
        for i in range(CHANNEL_COUNT):
            res.radiometrics.append(HritSubTagRadiometricProcessing.convertFromUfd(radiometrics[i]))
        return res

    def encode(self):
        buf = []
        for i in range(CHANNEL_COUNT):
            buf.append(self.radiometrics[i].encode())
        res = numpy.concatenate(buf)
        return res

    def decode(self, data, pos):
        for i in range(CHANNEL_COUNT):
            radiometric = HritSubTagRadiometricProcessing()
            pos = radiometric.decode(data, pos)
            self.radiometrics.append(radiometric)
        return pos
