from datetime import datetime, timezone

from ru.rks.meteo.Assist.MeteoAssist import DWORD_SIZE
from ru.rks.meteo.ufd.UfdRecord import UfdRecord, UFD_TAG_FileInfo, UFD_TAG_SatelliteStatus, UFD_TAG_ImageAcquisition, \
    UFD_TAG_RadiometricProcessing, UFD_TAG_GeometricProcessing, UFD_TAG_SeansISO, UFD_TAG_Image, UFD_TAG_SeansOKI, \
    UFD_TAG_GeoProjection
from ru.rks.meteo.ufd.tag.UfdTagFileInfo import UfdTagFileInfo
from ru.rks.meteo.ufd.tag.UfdTagGeoProjection import UfdTagGeoProjection
from ru.rks.meteo.ufd.tag.UfdTagGeometricProcessing import UfdTagGeometricProcessing
from ru.rks.meteo.ufd.tag.UfdTagImage import UfdTagImage
from ru.rks.meteo.ufd.tag.UfdTagImageAcquisition import UfdTagImageAcquisition
from ru.rks.meteo.ufd.tag.UfdTagRadiometricProcessing import UfdTagRadiometricProcessing
from ru.rks.meteo.ufd.tag.UfdTagSatelliteStatus import UfdTagSatelliteStatus
from ru.rks.meteo.ufd.tag.UfdTagSeansISO import UfdTagSeansISO
from ru.rks.meteo.ufd.tag.UfdTagSeansOKI import UfdTagSeansOKI

UFD_Signature = "UFD_MSU-GS_FILE"


def getTag(udfTagType):
    return {
        UFD_TAG_FileInfo: UfdTagFileInfo(),
        UFD_TAG_SatelliteStatus: UfdTagSatelliteStatus(),
        UFD_TAG_ImageAcquisition: UfdTagImageAcquisition(),
        UFD_TAG_RadiometricProcessing: UfdTagRadiometricProcessing(),
        UFD_TAG_GeometricProcessing: UfdTagGeometricProcessing(),
        UFD_TAG_SeansISO: UfdTagSeansISO(),
        UFD_TAG_Image: UfdTagImage(),
        UFD_TAG_SeansOKI: UfdTagSeansOKI(),
        UFD_TAG_GeoProjection: UfdTagGeoProjection()
    }.get(udfTagType, None)


class UfdDecoder:

    def __init__(self):
        self.pos = 0

    def decode(self, data):
        self.pos = 0
        ufd = UfdRecord()
        if not self.decodePreHead(data, ufd):
            return None
        self.decodeTags(data, ufd)
        return ufd

    def decodePreHead(self, data, ufd):
        res = self.parseString(data, len(UFD_Signature) + 1)
        if res != UFD_Signature:
            return False
        ufd.headVersion = self.parseDWORD(data)
        ufd.preHeadLength = self.parseDWORD(data)
        ufd.dataType = self.parseDWORD(data)
        ufd.receptionStation = self.parseString(data, 256)
        ufd.corp = self.parseString(data, 256)
        ufd.seansData = self.parseDate(data)
        ufd.seansDataEasy = self.parseString(data, 20)
        ufd.satNumber = self.parseDWORD(data)
        self.pos += 1000
        return True

    def decodeTags(self, data, ufd):
        while len(data) - self.pos > 8:
            tagType = self.parseDWORD(data)
            tagLength = self.parseDWORD(data)
            buf = data[self.pos:self.pos + tagLength - 8]
            self.pos += tagLength - 8
            tag = getTag(tagType)
            if tag is not None:
                tag.parse(buf)
                ufd.tags[tagType] = tag

    def parseString(self, data, size):
        sz = size
        while data[self.pos + sz - 1] == 0:
            sz -= 1
        buf = data[self.pos:self.pos + sz].ravel().tobytes()
        res = buf.decode('windows-1251')
        self.pos += size
        return res

    def parseDWORD(self, data):
        res = int.from_bytes(data[self.pos:self.pos + DWORD_SIZE], byteorder='little', signed=False)
        self.pos += DWORD_SIZE
        return res

    def parseDate(self, data):
        res = (self.parseDWORD(data) + datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc).timestamp()) * 1000
        return res
