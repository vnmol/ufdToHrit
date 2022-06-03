import datetime
import math

import numpy
from numpy import uint8

from ru.rks.meteo.hrit.body.HritBody import PROLOG, CHANNEL, EPILOG
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.hrit.header.HritHeader import HritHeader, ANNOTATION
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_SatelliteStatus, UFD_TAG_Image

fieldExtraChar = "_"
fieldSeparator = "-"


class HritHeaderAnnotation(HritHeader):

    def __init__(self):
        self.xritChannelID = ''
        self.disseminationID = ''
        self.disseminatingSC = ''
        self.productID1 = ''
        self.productID2 = ''
        self.productID3 = ''
        self.productID4 = ''
        self.flags = ''
        self.resolution = ''

    @staticmethod
    def convertFromUfd(file_type_code, ufd, resolution, segment):
        res = HritHeaderAnnotation()
        res.resolution = resolution
        res.xritChannelID = "H"
        res.disseminationID = "000"
        status = ufd.tags[UFD_TAG_SatelliteStatus]
        res.disseminatingSC = HritHeaderAnnotation.getDisseminatingSC(status.satelliteID)
        if file_type_code == PROLOG:
            res.productID1 = res.disseminatingSC + fieldExtraChar + resolution
            res.productID2 = ''
            res.productID3 = 'PRO'
        elif file_type_code == CHANNEL:
            res.productID1 = res.disseminatingSC + fieldExtraChar + str(ufd.getResolution())
            res.productID2 = HritHeaderAnnotation.getProductID2(status.nominalLongitude, ufd.tags[UFD_TAG_Image].tagChGroup)
            res.productID3 = '{:0>6d}'.format(segment + 1)
        elif file_type_code == EPILOG:
            res.productID1 = res.disseminatingSC + fieldExtraChar + resolution
            res.productID2 = ''
            res.productID3 = 'EPI'
        res.productID4 = HritHeaderAnnotation.getTime(ufd.seansData)
        res.flags = ''
        return res

    @staticmethod
    def getDisseminatingSC(satelliteID):
        if satelliteID == 19002:
            return 'GOMS2'
        elif satelliteID == 19003:
            return 'GOMS3'
        elif satelliteID == 3720:
            return 'ARCM1'
        return 'XXXXX'

    @staticmethod
    def getProductID2(nominalLongitude, channel):
        nl = math.degrees(nominalLongitude)
        suffix = '{:0>3d}'.format(int(abs(nl))) + 'W' if nl < 0 else 'E'
        res = 'XX_X_'
        if channel == 1500:
            res = '00_6_'
        elif channel == 1501:
            res = '00_7_'
        elif channel == 1502:
            res = '00_9_'
        elif channel == 1503:
            res = '03_8_'
        elif channel == 1504:
            res = '06_4_'
        elif channel == 1505:
            res = '10_7_'
        elif channel == 1506:
            res = '08_0_'
        elif channel == 1507:
            res = '11_9_'
        elif channel == 1508:
            res = '08_7_'
        elif channel == 1509:
            res = '09_7_'
        return res + suffix

    @staticmethod
    def getTime(secs):
        tm =  datetime.datetime.utcfromtimestamp(int(secs) // 1000)
        return tm.strftime('%Y%m%d%H%M')

    def decode(self, data):
        text = HritTag.decodeString(data)
        tokens = text.split(fieldSeparator)
        self.xritChannelID = self.unformat(tokens[0])
        self.disseminationID = self.unformat(tokens[1])
        self.disseminatingSC = self.unformat(tokens[2])
        self.productID1 = self.unformat(tokens[3])
        self.productID2 = self.unformat(tokens[4])
        self.productID3 = self.unformat(tokens[5])
        self.productID4 = self.unformat(tokens[6])
        self.flags = self.unformat(tokens[7])

    def encode(self):
        return HritHeader.encoding(ANNOTATION, numpy.frombuffer(self.getString().encode('windows-1251'), dtype=uint8))

    def getString(self):
        res = self.format(self.xritChannelID, 1) + fieldSeparator + \
              self.format(self.disseminationID, 3) + fieldSeparator + \
              self.format(self.disseminatingSC, 6) + fieldSeparator + \
              self.format(self.getProductID1(), 12) + fieldSeparator + \
              self.format(self.productID2, 9) + fieldSeparator + \
              self.format(self.productID3, 9) + fieldSeparator + \
              self.format(self.productID4, 12) + fieldSeparator + \
              self.format(self.flags, 2)
        return res

    def getProductID1(self):
        return self.disseminatingSC + fieldExtraChar + "4"

    @staticmethod
    def format(val, size):
        val += fieldExtraChar * (size - len(val))
        return val

    @staticmethod
    def unformat(val):
        return val.replace(fieldExtraChar, '')
