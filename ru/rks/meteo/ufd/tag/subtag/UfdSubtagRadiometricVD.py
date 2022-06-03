from ru.rks.meteo.ufd.tag.UfdTag import UfdTag


class UfdSubtagRadiometricVD(UfdTag):

    def __init__(self):
        super(UfdSubtagRadiometricVD, self).__init__()
        self.structNoiseCorrectionVD = []
        self.neravnCorrectionVD = []
        self.preFlightCalibrVD_Spectral = 0.0
        self.preFlightCalibrVD_Amplitude = []
        self.preFlightCalibrVD_Zone = []
        self.preFlightCalibrVD_StructSKO = []
        self.preFlightCalibrVD_TemnSKO = []
        self.preFlightCalibrVD_S_Noise = 0.0
        self.eathDarkeningErrorsVD = 0

    def parse(self, data, pos):
        self.pos = pos
        for i in range(12040):
            self.structNoiseCorrectionVD.append([])
            for j in range(2):
                self.structNoiseCorrectionVD[i].append(self.parseDouble(data))
        for i in range(16):
            self.neravnCorrectionVD.append(self.parseDouble(data))
        self.preFlightCalibrVD_Spectral = self.parseDouble(data)
        for i in range(2):
            self.preFlightCalibrVD_Amplitude.append(self.parseDouble(data))
        for i in range(3):
            self.preFlightCalibrVD_Zone.append(self.parseDouble(data))
        for i in range(2):
            self.preFlightCalibrVD_StructSKO.append(self.parseDouble(data))
        for i in range(2):
            self.preFlightCalibrVD_TemnSKO.append(self.parseDouble(data))
        self.preFlightCalibrVD_S_Noise = self.parseDouble(data)
        self.eathDarkeningErrorsVD = self.parseInt(data)
        return self.pos
