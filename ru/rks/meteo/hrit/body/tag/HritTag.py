import struct

import numpy
from numpy import uint8

from ru.rks.meteo.Assist.MeteoAssist import BYTE_SIZE, WORD_SIZE, DWORD_SIZE, QWORD_SIZE, INT_SIZE, BIGINT_SIZE, \
    DOUBLE_SIZE


class HritTag:

    @staticmethod
    def encodeNum(val, size):
        return numpy.frombuffer(val.to_bytes(size, byteorder='big'), dtype=uint8)

    @staticmethod
    def decodeNum(data):
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def encodeByte(val):
        return HritTag.encodeNum(val, BYTE_SIZE)

    @staticmethod
    def decodeByte(data):
        return HritTag.decodeNum(data)

    @staticmethod
    def encodeWORD(val):
        return HritTag.encodeNum(val, WORD_SIZE)

    @staticmethod
    def decodeWORD(data):
        return HritTag.decodeNum(data)

    @staticmethod
    def encodeDWORD(val):
        return HritTag.encodeNum(val, DWORD_SIZE)

    @staticmethod
    def decodeDWORD(data):
        return HritTag.decodeNum(data)

    @staticmethod
    def encodeQWORD(val):
        return HritTag.encodeNum(val, QWORD_SIZE)

    @staticmethod
    def decodeQWORD(data):
        return HritTag.decodeNum(data)

    @staticmethod
    def encodeInt(val):
        return numpy.frombuffer(val.to_bytes(INT_SIZE, byteorder='big', signed=True), dtype=uint8)


    @staticmethod
    def decodeInt(data):
        return int.from_bytes(data, byteorder='big', signed=True)

    @staticmethod
    def encodeBigInt(val):
        return numpy.frombuffer(val.to_bytes(BIGINT_SIZE, byteorder='little'), dtype=uint8)

    @staticmethod
    def decodeBigInt(data):
        return int.from_bytes(data, byteorder='little', signed=False)

    @staticmethod
    def encodeDouble(val):
        return numpy.frombuffer(struct.pack('d', val), dtype=uint8)

    @staticmethod
    def decodeDouble(data):
        return struct.unpack('d', data)[0]

    @staticmethod
    def encodeString(val, size):
        val = (val[:size - 1]) if len(val) > size - 1 else val
        data = val.encode('windows-1251')
        data += b'\0' * (size - len(data))
        res = numpy.frombuffer(data, dtype=uint8)
        return res

    @staticmethod
    def decodeString(data):
        return data.ravel().tobytes().decode('windows-1251').replace('\0', '')

    @staticmethod
    def encodeDoubleArray(val):
        buf = []
        for i in range(len(val)):
            buf.append(HritTag.encodeDouble(val[i]))
        res = numpy.concatenate(buf)
        return res

    @staticmethod
    def decodeDoubleArray(data, pos, val, length):
        for i in range(length):
            val.append(HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE]))
            pos += DOUBLE_SIZE
        return pos

    @staticmethod
    def getLength(buf):
        res = 0
        for part in buf:
            res += len(part)
        return res

    @staticmethod
    def encodeLength(buf):
        return HritTag.encodeDWORD(HritTag.getLength(buf))
