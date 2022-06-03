import numpy

from ru.rks.meteo.Assist.MeteoAssist import HIGH_BITS_PER_PIX, LOW_BITS_PER_PIX, SECTION_SIZE, BYTE_SIZE, WORD_SIZE
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.hrit.header.HritHeader import HritHeader, IMAGE_STRUCTURE
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_Image


class HritHeaderImageStructure(HritHeader):

    def __init__(self):
        self.nb = 0
        self.nc = 0
        self.nl = 0
        self.cflg = 0

    @staticmethod
    def convertFromUfd(ufd):
        res = HritHeaderImageStructure()
        tag = ufd.tags[UFD_TAG_Image]
        res.nb = HIGH_BITS_PER_PIX if tag.spkInfo_BitPerPix >= 10 else LOW_BITS_PER_PIX
        res.nc = tag.spkInfo_Width
        res.nl = SECTION_SIZE
        res.cflg = 0
        return res

    def decode(self, data):
        pos = 0
        self.nb = HritTag.decodeByte(data[pos:pos])
        pos += BYTE_SIZE
        self.nc = HritTag.decodeDWORD(data[pos:pos + WORD_SIZE])
        pos += WORD_SIZE
        self.nl = HritTag.decodeQWORD(data[pos:pos + WORD_SIZE])
        pos += WORD_SIZE
        self.cflg = HritTag.decodeByte(data[pos:pos])
        pos += BYTE_SIZE

    def encode(self):
        buf = []
        buf.append(HritTag.encodeByte(self.nb))
        buf.append(HritTag.encodeWORD(self.nc))
        buf.append(HritTag.encodeWORD(self.nl))
        buf.append(HritTag.encodeByte(self.cflg))
        res = numpy.concatenate(buf)
        res = HritHeader.encoding(IMAGE_STRUCTURE, res)
        return res
