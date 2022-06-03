from ru.rks.meteo.Assist.MeteoAssist import DOUBLE_SIZE, INT_SIZE
from ru.rks.meteo.ufd.tag.UfdTag import UfdTag


class UfdSubtagTISO(UfdTag):

    @staticmethod
    def getSize():
        return (1 + 1 + 1 + 3 * 3 * 4 + 4 * 6) * DOUBLE_SIZE + INT_SIZE;

    def __init__(self):
        super(UfdSubtagTISO, self).__init__()
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

    def parse(self, data, pos):
        self.pos = pos
        self.t0 = self.parseDouble(data)
        self.dT = self.parseDouble(data)
        self.aSb = self.parseDouble(data)
        for i in range(3):
            self.evsk.append([])
            for j in range(3):
                self.evsk[i].append([])
                for k in range(4):
                    self.evsk[i][j].append(self.parseDouble(data))
        for i in range(4): self.aRx.append(self.parseDouble(data))
        for i in range(4): self.aRy.append(self.parseDouble(data))
        for i in range(4): self.aRz.append(self.parseDouble(data))
        for i in range(4): self.aVx.append(self.parseDouble(data))
        for i in range(4): self.aVy.append(self.parseDouble(data))
        for i in range(4): self.aVz.append(self.parseDouble(data))
        self.type = self.parseInt(data)
        return self.pos
