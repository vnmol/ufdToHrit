import numpy

from ru.rks.meteo.Assist.MeteoAssist import DOUBLE_SIZE, INT_SIZE
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag


class HritSubTagTISO:

    def __init__(self):
        self.t0 = 0.0
        self.dT = 0.0
        self.aSb = 0.0
        self.evsk = []
        self.aRx = []
        self.aRy = []
        self.aRz = []
        self.aVx = []
        self.aVy = []
        self.aVz = []
        self.type = 0

    def convertFromUfd(self, satInfo):
        self.t0 = satInfo.t0
        self.dT = satInfo.dT
        self.aSb = satInfo.aSb
        self.evsk = satInfo.evsk
        self.aRx = satInfo.aRx
        self.aRy = satInfo.aRy
        self.aRz = satInfo.aRz
        self.aVx = satInfo.aVx
        self.aVy = satInfo.aVy
        self.aVz = satInfo.aVz
        self.type = satInfo.type

    def encode(self):
        buf = []
        buf.append(HritTag.encodeDouble(self.t0))
        buf.append(HritTag.encodeDouble(self.dT))
        buf.append(HritTag.encodeDouble(self.aSb))
        buf.append(self.encodeEvsk())
        buf.append(HritTag.encodeDoubleArray(self.aRx))
        buf.append(HritTag.encodeDoubleArray(self.aRy))
        buf.append(HritTag.encodeDoubleArray(self.aRz))
        buf.append(HritTag.encodeDoubleArray(self.aVx))
        buf.append(HritTag.encodeDoubleArray(self.aVy))
        buf.append(HritTag.encodeDoubleArray(self.aVz))
        buf.append(HritTag.encodeInt(self.type))
        res = numpy.concatenate(buf)
        return res

    def encodeEvsk(self):
        buf = []
        for i in range(3):
            for j in range(3):
                for k in range(4):
                    buf.append(HritTag.encodeDouble(self.evsk[i][j][k]))
        res = numpy.concatenate(buf)
        return res

    def decode(self, data, pos):
        self.t0 = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.dT = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.aSb = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        pos = self.decodeEvsk(data, pos)
        pos = HritTag.decodeDoubleArray(data, pos, self.aRx, 4)
        pos = HritTag.decodeDoubleArray(data, pos, self.aRy, 4)
        pos = HritTag.decodeDoubleArray(data, pos, self.aRz, 4)
        pos = HritTag.decodeDoubleArray(data, pos, self.aVx, 4)
        pos = HritTag.decodeDoubleArray(data, pos, self.aVy, 4)
        pos = HritTag.decodeDoubleArray(data, pos, self.aVz, 4)
        self.type = HritTag.decodeInt(data[pos:pos + INT_SIZE])
        pos += INT_SIZE
        return pos

    def decodeEvsk(self, data, pos):
        for i in range(3):
            self.evsk.append([])
            for j in range(3):
                self.evsk[i].append([])
                for k in range(4):
                    self.evsk[i][j].append(HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE]))
                    pos += DOUBLE_SIZE
        return pos
