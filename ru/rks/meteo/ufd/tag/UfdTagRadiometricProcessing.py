from ru.rks.meteo.ufd.tag.UfdTag import UfdTag
from ru.rks.meteo.ufd.tag.subtag.UfdSubtagRadiometricIR import UfdSubtagRadiometricIR
from ru.rks.meteo.ufd.tag.subtag.UfdSubtagRadiometricVD import UfdSubtagRadiometricVD


class UfdTagRadiometricProcessing(UfdTag):

    def __init__(self):
        super(UfdTagRadiometricProcessing, self).__init__()
        self.tagChGroup = 0
        self.rpSummary_Impulse = 0
        self.rpSummary_IsStrNoiseCorrection = 0
        self.rpSummary_IsNeravn = 0
        self.rpSummary_IsOptic = 0
        self.rpSummary_IsLinerial = 0
        self.rpSummary_IsBrightnessAligment = 0
        self.opticCorrection_Degree = 0
        self.opticCorrection_A = []
        self.opticCorrection_Linearization = []
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
        self.subtag = None
        self.reserved1 = []
        self.tacht = 0.0
        self.graduirovkaEasySignatura = ''
        self.graduirovkaEasy = []

    def parse(self, data):
        self.tagChGroup = self.parseDWORD(data)
        self.rpSummary_Impulse = self.parseDWORD(data)
        self.rpSummary_IsStrNoiseCorrection = self.parseDWORD(data)
        self.rpSummary_IsNeravn = self.parseDWORD(data)
        self.rpSummary_IsOptic = self.parseDWORD(data)
        self.rpSummary_IsLinerial = self.parseDWORD(data)
        self.rpSummary_IsBrightnessAligment = self.parseDWORD(data)
        self.opticCorrection_Degree = self.parseInt(data)
        for i in range(16):
            self.opticCorrection_A.append(self.parseDouble(data))
        for i in range(32):
            self.opticCorrection_Linearization.append(self.parseDouble(data))
        self.rpQuality_EffDinRange = self.parseDouble(data)
        self.rpQuality_EathDarkening = self.parseDouble(data)
        self.rpQuality_Zone = self.parseDouble(data)
        self.rpQuality_Impulse = self.parseDouble(data)
        self.rpQuality_Group = self.parseDouble(data)
        self.rpQuality_DefectCount = self.parseDWORD(data)
        self.rpQuality_DefectProcent = self.parseDouble(data)
        self.rpQuality_S_Noise_DT_Preflight = self.parseDouble(data)
        self.rpQuality_S_Noise_DT_Bort = self.parseDouble(data)
        self.rpQuality_S_Noise_DT_Video = self.parseDouble(data)
        self.rpQuality_S_Noise_DT_1_5 = self.parseDouble(data)
        self.rpQuality_CalibrStability = self.parseDouble(data)
        for i in range(2):
            self.rpQuality_TemnSKO.append(self.parseDouble(data))
        for i in range(2):
            self.rpQuality_StructSKO.append(self.parseDouble(data))
        self.rpQuality_Struct_1_5 = self.parseDouble(data)
        self.rpQuality_Zone_1_5 = self.parseDouble(data)
        self.rpQuality_RadDif = self.parseDouble(data)
        self.subtag = UfdSubtagRadiometricVD() if self.isVisible() else UfdSubtagRadiometricIR()
        self.pos = self.subtag.parse(data, self.pos)
        for i in range(1024):
            self.reserved1.append(self.parseDouble(data))
        self.tacht = self.parseDouble(data)
        self.graduirovkaEasySignatura = self.parseString(data, 64)
        for i in range(1024):
            self.graduirovkaEasy.append(self.parseInt(data))

    def isVisible(self):
        return self.tagChGroup in {1000, 1001, 1002, 1500, 1501, 1502}
