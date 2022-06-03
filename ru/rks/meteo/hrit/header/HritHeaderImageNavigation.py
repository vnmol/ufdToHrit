import math

import numpy

from ru.rks.meteo.Assist.MeteoAssist import DWORD_SIZE
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.hrit.header.HritHeader import HritHeader, IMAGE_NAVIGATION
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_GeometricProcessing


class HritHeaderImageNavigation(HritHeader):

    def __init__(self):
        self.projection_name = ''
        self.cfac = 0
        self.lfac = 0
        self.coff = 0
        self.loff = 0

    @staticmethod
    def convertFromUfd(ufd):
        res = HritHeaderImageNavigation()
        res.projection_name = 'GEOS<+000.0>'
        tag = ufd.tags[UFD_TAG_GeometricProcessing]
        x0 = tag.tGeomNormInfo_PixInfo[0]
        dx = tag.tGeomNormInfo_PixInfo[1]
        y0 = tag.tGeomNormInfo_PixInfo[2]
        dy = tag.tGeomNormInfo_PixInfo[3]
        res.cfac = int(math.pi * 0x10000 / (180 * dx))
        res.lfac = int(math.pi * 0x10000 / (180 * dy))
        res.coff = int(1 - x0 / dx)
        res.loff = int(1 - y0 / dy)
        return res

    def decode(self, data):
        pos = 0
        self.projection_name = HritTag.decodeString(data[pos:pos + 32])
        pos += 32
        self.cfac = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.lfac = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.coff = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.loff = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE

    def encode(self):
        buf = []
        buf.append(HritTag.encodeString(self.projection_name, 32))
        buf.append(HritTag.encodeDWORD(self.cfac))
        buf.append(HritTag.encodeDWORD(self.lfac))
        buf.append(HritTag.encodeDWORD(self.coff))
        buf.append(HritTag.encodeDWORD(self.loff))
        res = numpy.concatenate(buf)
        res = HritHeader.encoding(IMAGE_NAVIGATION, res)
        return res
