from ru.rks.meteo.ufd.tag.UfdTag import UfdTag
from ru.rks.meteo.ufd.tag.subtag.UfdSubtagTISO import UfdSubtagTISO


class UfdTagGeometricProcessing(UfdTag):

    def __init__(self):
        super(UfdTagGeometricProcessing, self).__init__()
        self.tagChGroup = 0
        self.tGeomNormInfo_IsExist = 0
        self.tGeomNormInfo_IsNorm = 0
        self.tGeomNormInfo_SubLon = 0.0
        self.tGeomNormInfo_TypeProjection = 0
        self.tGeomNormInfo_PixInfo = []
        self.satInfo = UfdSubtagTISO()
        self.timeProcessing = 0.0
        self.apriorAccuracy = 0.0
        self.relativeAccuracy = []
        self.geoTypeEx = 0
        self.geoTypeEx2 = 0
        self.isoComplite = 0.0
        self.time_PredObr = 0
        self.time_Radiometry = 0
        self.time_WaitISO = 0
        self.time_KPGP = 0
        self.time_NormGeom = 0
        self.selectIsoMsgCount = 0
        self.selectISO = UfdSubtagTISO()
        self.kpgpKorrecture = []
        self.selectOKIMsgCount = 0

    def parse(self, data):
        self.tagChGroup = self.parseDWORD(data)
        self.tGeomNormInfo_IsExist = self.parseDWORD(data)
        self.tGeomNormInfo_IsNorm = self.parseDWORD(data)
        self.tGeomNormInfo_SubLon = self.parseDouble(data)
        self.tGeomNormInfo_TypeProjection = self.parseDWORD(data)
        for i in range(4):
            self.tGeomNormInfo_PixInfo.append(self.parseDouble(data))
        self.pos = self.satInfo.parse(data, self.pos)
        self.timeProcessing = self.parseDouble(data)
        self.apriorAccuracy = self.parseDouble(data)
        for i in range(2):
            self.relativeAccuracy.append(self.parseDouble(data))
        self.geoTypeEx = self.parseDWORD(data)
        self.geoTypeEx2 = self.parseDWORD(data)
        self.isoComplite = self.parseDouble(data)
        self.time_PredObr = self.parseDWORD(data)
        self.time_Radiometry = self.parseDWORD(data)
        self.time_WaitISO = self.parseDWORD(data)
        self.time_KPGP = self.parseDWORD(data)
        self.time_NormGeom = self.parseDWORD(data)
        self.selectIsoMsgCount = self.parseInt(data)
        self.pos = self.selectISO.parse(data, self.pos)
        for i in range(16):
            self.kpgpKorrecture.append(self.parseDouble(data))
        self.selectOKIMsgCount = self.parseInt(data)
