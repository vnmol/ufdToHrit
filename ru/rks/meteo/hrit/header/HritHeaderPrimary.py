import numpy

from ru.rks.meteo.Assist.MeteoAssist import BYTE_SIZE, DWORD_SIZE, QWORD_SIZE
from ru.rks.meteo.hrit.body import HritBody
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.hrit.header.HritHeader import HritHeader
from ru.rks.meteo.hrit.header.HritHeaderFactory import PRIMARY_HEADER


class HritHeaderPrimary(HritHeader):

    def __init__(self):
        self.file_type_code = HritBody.CHANNEL
        self.total_header_length = 0
        self.data_field_length = 0

    @staticmethod
    def convertFromUfd(file_type_code):
        res = HritHeaderPrimary()
        res.file_type_code = file_type_code
        return res

    def decode(self, data):
        pos = 0
        self.total_header_length = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.data_field_length = HritTag.decodeQWORD(data[pos:pos + QWORD_SIZE])
        pos += QWORD_SIZE

    def encode(self):
        buf = []
        buf.append(HritTag.encodeByte(self.file_type_code))
        buf.append(HritTag.encodeDWORD(self.total_header_length))
        buf.append(HritTag.encodeQWORD(self.data_field_length))
        res = numpy.concatenate(buf)
        res = HritHeader.encoding(PRIMARY_HEADER, res)
        return res
