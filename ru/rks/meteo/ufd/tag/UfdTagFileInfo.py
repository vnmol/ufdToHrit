from ru.rks.meteo.ufd.tag.UfdTag import UfdTag


class UfdTagFileInfo(UfdTag):

    def __init__(self):
        super(UfdTagFileInfo, self).__init__()
        self.inChs = []
        self.outChs = []

    def parse(self, data):
        for i in range(6):
            self.inChs.append(self.parseDWORD(data))
        for i in range(10):
            self.outChs.append(self.parseDWORD(data))
