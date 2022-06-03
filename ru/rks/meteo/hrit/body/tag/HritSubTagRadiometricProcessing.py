import numpy

from ru.rks.meteo.Assist.MeteoAssist import DWORD_SIZE, INT_SIZE, DOUBLE_SIZE
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_RadiometricProcessing


class HritSubTagRadiometricProcessing:

    def __init__(self):
        self.rpSummary_Impulse = 0
        self.rpSummary_IsStrNoiseCorrection = 0
        self.rpSummary_IsOptic = 0
        self.rpSummary_IsBrightnessAligment = 0
        self.opticCorrection_Degree = 0
        self.opticCorrection_A = []
        self.rpQuality_EffDinRange = 0.0
        self.rpQuality_EathDarkening = 0.0
        self.rpQuality_Zone = 0.0
        self.rpQuality_Impulse = 0.0
        self.rpQuality_Group = 0.0
        self.rpQuality_DefectCount = 0
        self.rpQuality_DefectProcent = 0.0
        self.rpQuality_S_Noise_DT_Preflight = 0.0
        self.rpQuality_S_Noise_DT_Bort = 0.0
        self.rpQuality_S_Noise_DT_Video = 0.0
        self.rpQuality_S_Noise_DT_1_5 = 0.0
        self.rpQuality_CalibrStability = 0.0
        self.rpQuality_TemnSKO = []
        self.rpQuality_StructSKO = []
        self.rpQuality_Struct_1_5 = 0.0
        self.rpQuality_Zone_1_5 = 0.0
        self.rpQuality_RadDif = 0.0

    @staticmethod
    def convertFromUfd(radiometric):
        res = HritSubTagRadiometricProcessing()
        res.rpSummary_Impulse = radiometric.rpSummary_Impulse
        res.rpSummary_IsStrNoiseCorrection = radiometric.rpSummary_IsStrNoiseCorrection
        res.rpSummary_IsOptic = radiometric.rpSummary_IsOptic
        res.rpSummary_IsBrightnessAligment = radiometric.rpSummary_IsBrightnessAligment
        res.opticCorrection_Degree = radiometric.opticCorrection_Degree
        res.opticCorrection_A = radiometric.opticCorrection_A
        res.rpQuality_EffDinRange = radiometric.rpQuality_EffDinRange
        res.rpQuality_EathDarkening = radiometric.rpQuality_EathDarkening
        res.rpQuality_Zone = radiometric.rpQuality_Zone
        res.rpQuality_Impulse = radiometric.rpQuality_Impulse
        res.rpQuality_Group = radiometric.rpQuality_Group
        res.rpQuality_DefectCount = radiometric.rpQuality_DefectCount
        res.rpQuality_DefectProcent = radiometric.rpQuality_DefectProcent
        res.rpQuality_S_Noise_DT_Preflight = radiometric.rpQuality_S_Noise_DT_Preflight
        res.rpQuality_S_Noise_DT_Bort = radiometric.rpQuality_S_Noise_DT_Bort
        res.rpQuality_S_Noise_DT_Video = radiometric.rpQuality_S_Noise_DT_Video
        res.rpQuality_S_Noise_DT_1_5 = radiometric.rpQuality_S_Noise_DT_1_5
        res.rpQuality_CalibrStability = radiometric.rpQuality_CalibrStability
        res.rpQuality_TemnSKO = radiometric.rpQuality_TemnSKO
        res.rpQuality_StructSKO = radiometric.rpQuality_StructSKO
        res.rpQuality_Struct_1_5 = radiometric.rpQuality_Struct_1_5
        res.rpQuality_Zone_1_5 = radiometric.rpQuality_Zone_1_5
        res.rpQuality_RadDif = radiometric.rpQuality_RadDif
        return res


    def encode(self):
        buf = []
        buf.append(HritTag.encodeDWORD(UFD_TAG_RadiometricProcessing))
        buf.append(HritTag.encodeDWORD(0))
        buf.append(HritTag.encodeDWORD(self.rpSummary_Impulse))
        buf.append(HritTag.encodeDWORD(self.rpSummary_IsStrNoiseCorrection))
        buf.append(HritTag.encodeDWORD(self.rpSummary_IsOptic))
        buf.append(HritTag.encodeDWORD(self.rpSummary_IsBrightnessAligment))
        buf.append(HritTag.encodeInt(self.opticCorrection_Degree))
        buf.append(HritTag.encodeDoubleArray(self.opticCorrection_A))
        buf.append(HritTag.encodeDouble(self.rpQuality_EffDinRange))
        buf.append(HritTag.encodeDouble(self.rpQuality_EathDarkening))
        buf.append(HritTag.encodeDouble(self.rpQuality_Zone))
        buf.append(HritTag.encodeDouble(self.rpQuality_Impulse))
        buf.append(HritTag.encodeDouble(self.rpQuality_Group))
        buf.append(HritTag.encodeDWORD(self.rpQuality_DefectCount))
        buf.append(HritTag.encodeDouble(self.rpQuality_DefectProcent))
        buf.append(HritTag.encodeDouble(self.rpQuality_S_Noise_DT_Preflight))
        buf.append(HritTag.encodeDouble(self.rpQuality_S_Noise_DT_Bort))
        buf.append(HritTag.encodeDouble(self.rpQuality_S_Noise_DT_Video))
        buf.append(HritTag.encodeDouble(self.rpQuality_S_Noise_DT_1_5))
        buf.append(HritTag.encodeDouble(self.rpQuality_CalibrStability))
        buf.append(HritTag.encodeDoubleArray(self.rpQuality_TemnSKO))
        buf.append(HritTag.encodeDoubleArray(self.rpQuality_StructSKO))
        buf.append(HritTag.encodeDouble(self.rpQuality_Struct_1_5))
        buf.append(HritTag.encodeDouble(self.rpQuality_Zone_1_5))
        buf.append(HritTag.encodeDouble(self.rpQuality_RadDif))
        buf[1] = HritTag.encodeLength(buf)
        res = numpy.concatenate(buf)
        return res

    def decode(self, data, pos):
        pos += DWORD_SIZE
        pos += DWORD_SIZE
        self.rpSummary_Impulse = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.rpSummary_IsStrNoiseCorrection = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.rpSummary_IsOptic = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.rpSummary_IsBrightnessAligment = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.opticCorrection_Degree = HritTag.decodeInt(data[pos:pos + INT_SIZE])
        pos += INT_SIZE
        pos = HritTag.decodeDoubleArray(data, pos, self.opticCorrection_A, 16)
        self.rpQuality_EffDinRange = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_EathDarkening =  HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_Zone =  HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_Impulse =  HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_Group =  HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_DefectCount = HritTag.decodeDWORD(data[pos:pos + DWORD_SIZE])
        pos += DWORD_SIZE
        self.rpQuality_DefectProcent = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_S_Noise_DT_Preflight = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_S_Noise_DT_Bort = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_S_Noise_DT_Video = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_S_Noise_DT_1_5 = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_CalibrStability = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        pos = HritTag.decodeDoubleArray(data, pos, self.rpQuality_TemnSKO, 2)
        pos = HritTag.decodeDoubleArray(data, pos, self.rpQuality_StructSKO, 2)
        self.rpQuality_Struct_1_5 = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_Zone_1_5 = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        self.rpQuality_RadDif = HritTag.decodeDouble(data[pos:pos + DOUBLE_SIZE])
        pos += DOUBLE_SIZE
        return pos
