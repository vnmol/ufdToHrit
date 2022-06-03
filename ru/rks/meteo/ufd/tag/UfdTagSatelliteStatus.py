from ru.rks.meteo.ufd.tag.UfdTag import UfdTag


class UfdTagSatelliteStatus(UfdTag):

    def __init__(self):
        super(UfdTagSatelliteStatus, self).__init__()
        self.satelliteID = 0
        self.satelliteName = ''
        self.nominalLongitude = 0.0
        self.satelliteCondition = 0
        self.timeOffset = 0.0

    def parse(self, data):
        self.satelliteID = self.parseQWORD(data)
        self.satelliteName = self.parseString(data, 256)
        self.nominalLongitude = self.parseDouble(data)
        self.satelliteCondition = self.parseDWORD(data)
        self.timeOffset = self.parseDouble(data)
