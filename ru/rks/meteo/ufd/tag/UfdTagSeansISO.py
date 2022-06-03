from ru.rks.meteo.ufd.tag.UfdTag import UfdTag
from ru.rks.meteo.ufd.tag.subtag.UfdSubtagTISO import UfdSubtagTISO


class UfdTagSeansISO(UfdTag):

    def __init__(self):
        super(UfdTagSeansISO, self).__init__()
        self.nAdded = 0
        self.nError = 0
        self.iso = []

    def parse(self, data):
        self.nAdded = self.parseInt(data)
        self.nError = self.parseInt(data)
        while len(data) - self.pos >= UfdSubtagTISO.getSize():
            iso = UfdSubtagTISO()
            self.pos = iso.parse(data, self.pos)
            self.iso.append(iso)
