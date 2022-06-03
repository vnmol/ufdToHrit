import numpy

from ru.rks.meteo.Assist.MeteoAssist import CHANNEL_COUNT, INT_SIZE
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag


class HritTagImageCalibration:

    def __init__(self):
        self.imageCalibration = []

    @staticmethod
    def convertFromUfd(ufdImageCalibration):
        res = HritTagImageCalibration()
        res.imageCalibration = ufdImageCalibration
        return res

    def encode(self):
        buf = []
        for i in range(len(self.imageCalibration)):
            b = []
            for j in range(len(self.imageCalibration[i])):
                b.append(HritTag.encodeInt(self.imageCalibration[i][j]))
            buf.append(numpy.concatenate(b))
        res = numpy.concatenate(buf)
        return res

    def decode(self, data, pos):
        for i in range(CHANNEL_COUNT):
            b = []
            for j in range(1024):
                b.append(HritTag.decodeInt(data[pos:pos + INT_SIZE]))
                pos += INT_SIZE
        return pos
