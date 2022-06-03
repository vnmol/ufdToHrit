from ru.rks.meteo.ufd.tag.UfdTag import UfdTag


class UfdSubtagRadiometricIR(UfdTag):

    def __init__(self):
        super(UfdSubtagRadiometricIR, self).__init__()
        self.StructNoiseCorrectionIR = []
        self.preFlightCalibrIR_Grad = []
        self.preFlightCalibrIR_DT = 0.0

    def parse(self, data, pos):
        self.pos = pos
        for i in range(192):
            self.StructNoiseCorrectionIR.append([])
            for j in range(2):
                self.StructNoiseCorrectionIR[i].append(self.parseDouble(data))
        for i in range(2):
            self.preFlightCalibrIR_Grad.append(self.parseDouble(data))
        self.preFlightCalibrIR_DT = self.parseDouble(data)
        return self.pos
