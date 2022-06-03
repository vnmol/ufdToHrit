import numpy

from ru.rks.meteo.Assist.MeteoAssist import CHANNEL_COUNT
from ru.rks.meteo.hrit.body.tag.HritSubTagImageAcquisition import HritSubTagImageAcquisition


class HritTagImageAcquisition:

    def __init__(self):
        self.imageAcquisitions = []

    @staticmethod
    def convertFromUfd(ufdImageAcquisitions):
        res = HritTagImageAcquisition()
        for i in range(CHANNEL_COUNT):
            res.imageAcquisitions.append(HritSubTagImageAcquisition.convertFromUfd(ufdImageAcquisitions[i]))
        return res

    def encode(self):
        buf = []
        for i in range(CHANNEL_COUNT):
            buf.append(self.imageAcquisitions[i].encode())
        res = numpy.concatenate(buf)
        return res

    def decode(self, data, pos):
        for i in range(CHANNEL_COUNT):
            acquisition = HritSubTagImageAcquisition()
            pos = acquisition.decode(data, pos)
            self.imageAcquisitions.append(acquisition)
        return pos
