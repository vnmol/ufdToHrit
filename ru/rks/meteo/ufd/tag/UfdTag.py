import struct
from datetime import datetime, timezone

from numpy import ndarray

from ru.rks.meteo.Assist.MeteoAssist import DWORD_SIZE, DOUBLE_SIZE, INT_SIZE, WORD_SIZE, QWORD_SIZE


class UfdTag:

    def __init__(self):
        self.pos = 0

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
                res += str(item[1]).strip('\r\n')
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

    def parseWORD(self, data):
        res = int.from_bytes(data[self.pos:self.pos + WORD_SIZE], byteorder='little', signed=False)
        self.pos += WORD_SIZE
        return res

    def parseDWORD(self, data):
        res = int.from_bytes(data[self.pos:self.pos + DWORD_SIZE], byteorder='little', signed=False)
        self.pos += DWORD_SIZE
        return res

    def parseQWORD(self, data):
        res = int.from_bytes(data[self.pos:self.pos + QWORD_SIZE], byteorder='little', signed=False)
        self.pos += QWORD_SIZE
        return res

    def parseInt(self, data):
        res = int.from_bytes(data[self.pos:self.pos + INT_SIZE], byteorder='little', signed=True)
        self.pos += INT_SIZE
        return res

    def parseDouble(self, data):
        res = struct.unpack('d', data[self.pos:self.pos + DOUBLE_SIZE])[0]
        self.pos += DOUBLE_SIZE
        return res

    def parseDate(self, data):
        res = (int(self.parseDouble(data) + datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc).timestamp())) * 1000
        return res

    def parseString(self, data, size):
        sz = size
        while data[self.pos + sz - 1] == 0:
            sz -= 1
        buf = data[self.pos:self.pos + sz].ravel().tobytes()
        res = buf.decode('windows-1251')
        self.pos += size
        return res
