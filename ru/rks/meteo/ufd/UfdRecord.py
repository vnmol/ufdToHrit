from ru.rks.meteo.Assist.MeteoAssist import HIGH_RESOLUTION


UFD_TAG_FileInfo              = 1
UFD_TAG_SatelliteStatus       = 2
UFD_TAG_ImageAcquisition      = 3
UFD_TAG_RadiometricProcessing = 4
UFD_TAG_GeometricProcessing   = 5
UFD_TAG_SeansISO              = 6
UFD_TAG_Image                 = 7
UFD_TAG_SeansOKI              = 8
UFD_TAG_GeoProjection         = 9


class UfdRecord:

    def __init__(self):
        self.headVersion = 0
        self.preHeadLength = 0
        self.dataType = 0
        self.receptionStation = ''
        self.corp = ""
        self.seansData = 0
        self.seansDataEasy = ''
        self.satNumber = 0
        self.tags = {}

    def __str__(self):
        res = type(self).__name__ + '{'
        flag = False
        for item in vars(self).items():
            if flag:
                res += ', '
            else:
                flag = True
            res += item[0] + '='
            if isinstance(item[1], dict):
                res += self.dict_str(item[1])
            else:
                res += str(item[1])
        res += '}'
        return res

    def dict_str(self, tags):
        res = '{'
        flag = False
        for indx in tags:
            if flag:
                res += ', '
            else:
                flag = True
            res += '\n' + str(indx) + '=' + str(tags[indx])
        res += '}'
        return res

    def getResolution(self):
        tag = self.tags[UFD_TAG_Image]
        res = 1 if tag.spkInfo_Width == HIGH_RESOLUTION \
                   and tag.spkInfo_Height == HIGH_RESOLUTION \
                   and tag.spkInfo_BitPerPix >= 10 else 4
        return res
