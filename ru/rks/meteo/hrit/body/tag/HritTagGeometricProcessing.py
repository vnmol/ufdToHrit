import numpy

from ru.rks.meteo.Assist.MeteoAssist import CHANNEL_COUNT
from ru.rks.meteo.hrit.body.tag.HritSubTagGeometricProcessing import HritSubTagGeometricProcessing


class HritTagGeometricProcessing:

    def __init__(self):
        self.geometrics = []

    @staticmethod
    def convertFromUfd(geometrics):
        res = HritTagGeometricProcessing()
        for i in range(CHANNEL_COUNT):
            res.geometrics.append(HritSubTagGeometricProcessing.convertFromUfd(geometrics[i]))
        return res

    def encode(self):
        buf = []
        for i in range(CHANNEL_COUNT):
            buf.append(self.geometrics[i].encode())
        res = numpy.concatenate(buf)
        return res

    def decode(self, data, pos):
        for i in range(CHANNEL_COUNT):
            geometric = HritSubTagGeometricProcessing()
            pos = geometric.decode(data, pos)
            self.geometrics.append(geometric)
        return pos

