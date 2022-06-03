import numpy

from ru.rks.meteo.Assist.MeteoAssist import DWORD_SIZE, QWORD_SIZE, BIGINT_SIZE, DOUBLE_SIZE
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_SatelliteStatus


class HritTagSatelliteStatus:

    def __init__(self):
        self.satelliteID = 0
        self.satelliteName = ''
        self.nominalLongitude = 0.0
        self.satelliteCondition = 0
        self.timeOffset = 0.0

    @staticmethod
    def convertFromUfd(ufd):
        status = ufd.tags[UFD_TAG_SatelliteStatus]
        res = HritTagSatelliteStatus()
        res.satelliteID = status.satelliteID
        res.satelliteName = status.satelliteName
        res.nominalLongitude = status.nominalLongitude
        res.satelliteCondition = status.satelliteCondition
        res.timeOffset = status.timeOffset
        return res

    def encode(self):
        buf = []
        buf.append(HritTag.encodeDWORD(UFD_TAG_SatelliteStatus))
        buf.append(HritTag.encodeDWORD(0))
        buf.append(HritTag.encodeBigInt(self.satelliteID))
        buf.append(HritTag.encodeString(self.satelliteName, 256))
        buf.append(HritTag.encodeDouble(self.nominalLongitude))
        buf.append(HritTag.encodeDWORD(self.satelliteCondition))
        buf.append(HritTag.encodeDouble(self.timeOffset))
        buf[1] = HritTag.encodeLength(buf)
        res = numpy.concatenate(buf)
        return res

    def decode(self, data, pos):
        pos += DWORD_SIZE
        pos += DWORD_SIZE
        self.satelliteID = HritTag.decodeBigInt(data[pos:pos + BIGINT_SIZE])
        pos += BIGINT_SIZE
        self.satelliteName = HritTag.decodeString(data[pos:pos + 256])
        pos += 256
        self.nominalLongitude = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.satelliteCondition = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.timeOffset = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        return pos
