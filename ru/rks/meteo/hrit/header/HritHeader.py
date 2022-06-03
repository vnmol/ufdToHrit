import numpy
from numpy import ndarray

from ru.rks.meteo.hrit.body.tag.HritTag import HritTag


PRIMARY_HEADER = 0
IMAGE_STRUCTURE = 1
IMAGE_NAVIGATION = 2
IMAGE_DATA_FUNCTION = 3
ANNOTATION = 4
TIME_STAMP = 5
ANCILLARY_TEXT = 6
KEY_HEADER = 7
SEGMENT_IDENTIFICATION = 128
IMAGE_SEGMENT_LINE_QUALITY = 129


class HritHeader:

    def encoding(headerType, buf):
        packet = []
        packet.append(HritTag.encodeByte(headerType))
        packet.append(HritTag.encodeWORD(0))
        packet.append(buf)
        length = HritTag.getLength(packet)
        packet[1] = HritTag.encodeWORD(length)
        res = numpy.concatenate(packet)
        return res

    def __str__(self) -> str:
        res = type(self).__name__ + '{'
        flag = False
        for item in vars(self).items():
            if flag:
                res += ', '
            else:
                flag = True
            res += item[0] + '='
            if isinstance(item[1], list):
                res += self.listPrint(item[1])
            elif isinstance(item[1], ndarray):
                res += self.ndarrayPrint(item[1])
            else:
                res += str(item[1])
        res += '}'
        return res

    def listPrint(self, item):
        res = '['
        length = len(item)
        if length > 10:
            length = 10
        flag = False
        for i in range(length):
            if flag:
                res += ', '
            else:
                flag = True
            if isinstance(item[i], list):
                res += self.listPrint(item[i])
            elif isinstance(item[i], ndarray):
                res += self.ndarrayPrint(item[i])
            else:
                res += str(item[i])
        if len(item) > length:
            res += ', ...'
        res += ']'
        return res

    def ndarrayPrint(self, item):
        res = '['
        length = len(item)
        if length > 10:
            length = 10
        flag = False
        for i in range(length):
            if flag:
                res += ', '
            else:
                flag = True
            if isinstance(item[i], list):
                res += self.listPrint(item[i])
            elif isinstance(item[i], ndarray):
                res += self.ndarrayPrint(item[i])
            else:
                res += str(item[i])
        if len(item) > length:
            res += ', ...'
        res += ']'
        return res


