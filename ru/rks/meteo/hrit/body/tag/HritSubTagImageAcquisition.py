import numpy

from ru.rks.meteo.Assist.MeteoAssist import DWORD_SIZE, DOUBLE_SIZE, INT_SIZE
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_ImageAcquisition


class HritSubTagImageAcquisition:

    def __init__(self):
        self.status = 0
        self.startDelay = 0
        self.cel = 0.0

    @staticmethod
    def convertFromUfd(ufdImageAcquisition):
        res = HritSubTagImageAcquisition()
        res.status = ufdImageAcquisition.status
        res.startDelay = ufdImageAcquisition.startDelay
        res.cel = ufdImageAcquisition.sboysDolya
        return res

    def encode(self):
        buf = []
        buf.append(HritTag.encodeDWORD(UFD_TAG_ImageAcquisition))
        buf.append(HritTag.encodeDWORD(0))
        buf.append(HritTag.encodeDWORD(self.status))
        buf.append(HritTag.encodeInt(self.startDelay))
        buf.append(HritTag.encodeDouble(self.cel))
        buf[1] = HritTag.encodeLength(buf)
        res = numpy.concatenate(buf)
        return res

    def decode(self, data, pos):
        pos += DWORD_SIZE
        pos += DWORD_SIZE
        self.status = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.startDelay = HritTag.decodeInt(data[pos:pos + INT_SIZE])
        pos += INT_SIZE
        self.cel = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        return pos
