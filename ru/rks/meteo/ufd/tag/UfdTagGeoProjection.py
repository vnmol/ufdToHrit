from ru.rks.meteo.ufd.tag.UfdTag import UfdTag


class UfdTagGeoProjection(UfdTag):

    def __init__(self):
        super(UfdTagGeoProjection, self).__init__()
        self.tagChGroup = 0
        self.typeProjection = 0
        self.pixInfo = []
        self.virtualKAPosition = []
        self.virtualKAOrient = []

    def parse(self, data):
        self.tagChGroup = self.parseDWORD(data)
        self.typeProjection = self.parseDWORD(data)
        for i in range(4):
            self.pixInfo.append(self.parseDouble(data))
        for i in range(3):
            self.virtualKAPosition.append(self.parseDouble(data))
        for i in range(3):
            self.virtualKAOrient.append([])
            for j in range(3):
                self.virtualKAOrient[i].append(self.parseDouble(data))
