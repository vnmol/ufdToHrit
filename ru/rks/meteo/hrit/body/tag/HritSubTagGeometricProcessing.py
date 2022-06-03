import numpy

from ru.rks.meteo.Assist.MeteoAssist import DWORD_SIZE, DOUBLE_SIZE
from ru.rks.meteo.hrit.body.tag.HritSubTagTISO import HritSubTagTISO
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_GeometricProcessing


class HritSubTagGeometricProcessing:

    def __init__(self):
        self.tagChGroup = 0
        self.tGeomNormInfo_IsExist = 0
        self.tGeomNormInfo_IsNorm = 0
        self.tGeomNormInfo_SubLon = 0.0
        self.tGeomNormInfo_TypeProjection = 0
        self.tGeomNormInfo_PixInfo = []
        self.satInfo = HritSubTagTISO()
        self.timeProcessing = 0.0
        self.apriorAccuracy = 0.0
        self.relativeAccuracy = []

    @staticmethod
    def convertFromUfd(geometric):
        res = HritSubTagGeometricProcessing()
        res.tagChGroup = geometric.tagChGroup
        res.tGeomNormInfo_IsExist = geometric.tGeomNormInfo_IsExist
        res.tGeomNormInfo_IsNorm = geometric.tGeomNormInfo_IsNorm
        res.tGeomNormInfo_SubLon = geometric.tGeomNormInfo_SubLon
        res.tGeomNormInfo_TypeProjection = geometric.tGeomNormInfo_TypeProjection
        res.tGeomNormInfo_PixInfo = geometric.tGeomNormInfo_PixInfo
        res.satInfo.convertFromUfd(geometric.satInfo)
        res.timeProcessing = geometric.timeProcessing
        res.apriorAccuracy = geometric.apriorAccuracy
        res.relativeAccuracy = geometric.relativeAccuracy
        return res

    def encode(self):
        buf = []
        buf.append(HritTag.encodeDWORD(UFD_TAG_GeometricProcessing))
        buf.append(HritTag.encodeDWORD(0))
        buf.append(HritTag.encodeDWORD(self.tagChGroup))
        buf.append(HritTag.encodeDWORD(self.tGeomNormInfo_IsExist))
        buf.append(HritTag.encodeDWORD(self.tGeomNormInfo_IsNorm))
        buf.append(HritTag.encodeDouble(self.tGeomNormInfo_SubLon))
        buf.append(HritTag.encodeDWORD(self.tGeomNormInfo_TypeProjection))
        buf.append(HritTag.encodeDoubleArray(self.tGeomNormInfo_PixInfo))
        buf.append(self.satInfo.encode())
        buf.append(HritTag.encodeDouble(self.timeProcessing))
        buf.append(HritTag.encodeDouble(self.apriorAccuracy))
        buf.append(HritTag.encodeDoubleArray(self.relativeAccuracy))
        buf[1] = HritTag.encodeLength(buf)
        res = numpy.concatenate(buf)
        return res

    def decode(self, data, pos):
        pos += DWORD_SIZE
        pos += DWORD_SIZE
        self.tagChGroup = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.tGeomNormInfo_IsExist = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        self.tGeomNormInfo_IsNorm = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        self.tGeomNormInfo_SubLon = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        self.tGeomNormInfo_TypeProjection = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos = HritTag.decodeDoubleArray(data, pos, self.tGeomNormInfo_PixInfo, 4)
        pos = self.satInfo.decode(data, pos)
        self.timeProcessing = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        self.apriorAccuracy = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos = HritTag.decodeDoubleArray(data, pos, self.relativeAccuracy, 2)
        return pos
