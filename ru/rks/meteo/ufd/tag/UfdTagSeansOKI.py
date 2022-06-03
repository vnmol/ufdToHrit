from ru.rks.meteo.ufd.tag.UfdTag import UfdTag


class UfdTagSeansOKI(UfdTag):

    def __init__(self):
        super(UfdTagSeansOKI, self).__init__()
        self.nAdded = 0
        self.nError = 0
        self.translated = 0
        self.recordSize = 0
        self.reserved = []
        self.oki = []

    def parse(self, data):
        self.nAdded = self.parseInt(data)
        self.nError = self.parseInt(data)
        self.translated = self.parseInt(data)
        self.recordSize = self.parseInt(data)
        for i in range(8):
            self.reserved.append(self.parseDWORD(data))
        while len(data) - self.pos >= self.recordSize:
            self.oki.append(data[self.pos:self.pos + self.recordSize])
            self.pos += self.recordSize
