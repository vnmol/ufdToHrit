import numpy

from ru.rks.meteo.Assist.MeteoAssist import WORD_SIZE, BYTE_SIZE
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.hrit.header.HritHeader import HritHeader, SEGMENT_IDENTIFICATION
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_SatelliteStatus


class HritHeaderSegmentIdentification(HritHeader):

    def __init__(self):
        self.gp_sc_id = 0
        self.spectral_Channel_ID = 0
        self.segm_Seq_No = 0
        self.planned_Start_Segm_Seq_No = 0
        self.planned_End_Segm_Seq_No = 0
        self.data_Field_Representation = 0

    @staticmethod
    def convertFromUfd(ufd, channelID, segment, segment_count):
        res = HritHeaderSegmentIdentification()
        res.gp_sc_id = ufd.tags[UFD_TAG_SatelliteStatus].satelliteID
        res.spectral_Channel_ID = channelID
        res.segm_Seq_No = segment + 1;
        res.planned_Start_Segm_Seq_No = 1;
        res.planned_End_Segm_Seq_No = segment_count
        res.data_Field_Representation = 0
        return res

    def decode(self, data):
        pos = 0
        self.gp_sc_id = HritTag.decodeWORD(data[pos:pos + WORD_SIZE])
        pos += WORD_SIZE
        self.spectral_Channel_ID = HritTag.decodeByte(data[pos:pos])
        pos += BYTE_SIZE
        self.segm_Seq_No = HritTag.decodeWORD(data[pos:pos + WORD_SIZE])
        pos += WORD_SIZE
        self.planned_Start_Segm_Seq_No = HritTag.decodeWORD(data[pos:pos + WORD_SIZE])
        pos += WORD_SIZE
        self.planned_End_Segm_Seq_No = HritTag.decodeWORD(data[pos:pos + WORD_SIZE])
        pos += WORD_SIZE
        self.data_Field_Representation = HritTag.decodeByte(data[pos:pos])
        pos += BYTE_SIZE

    def encode(self):
        buf = []
        buf.append(HritTag.encodeWORD(self.gp_sc_id))
        buf.append(HritTag.encodeByte(self.spectral_Channel_ID))
        buf.append(HritTag.encodeWORD(self.segm_Seq_No))
        buf.append(HritTag.encodeWORD(self.planned_Start_Segm_Seq_No))
        buf.append(HritTag.encodeWORD(self.planned_End_Segm_Seq_No))
        buf.append(HritTag.encodeByte(self.data_Field_Representation))
        res = numpy.concatenate(buf)
        res = HritHeader.encoding(SEGMENT_IDENTIFICATION, res)
        return res
