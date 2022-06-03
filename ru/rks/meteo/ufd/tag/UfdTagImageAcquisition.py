from ru.rks.meteo.ufd.tag.UfdTag import UfdTag


class UfdTagImageAcquisition(UfdTag):

    def __init__(self):
        super(UfdTagImageAcquisition, self).__init__()
        self.tagChGroup = 0
        self.status = 0
        self.startAcquisitionTime = 0
        self.endAcquisitionTime = 0
        self.sboysDolya = 0.0
        self.temp = []
        self.yMode = 0
        self.fm_LinesPerSecond = 0.0
        self.errsPSP = 0
        self.errsLine = 0
        self.errsBSHV = 0
        self.chMask = []
        self.isCanContinueWork = False
        self.errorText = ''
        self.priborNomerCode = 0
        self.dupErrorScansN = 0
        self.tachtIRCode = 0.0
        self.startDelay = 0

    def parse(self, data):
        self.tagChGroup = self.parseDWORD(data)
        self.status = self.parseDWORD(data)
        self.startAcquisitionTime = self.parseDate(data)
        self.endAcquisitionTime = self.parseDate(data)
        self.sboysDolya = self.parseDouble(data)
        for i in range(32):
            self.temp.append(self.parseDWORD(data))
        self.yMode = self.parseDWORD(data)
        self.fm_LinesPerSecond = self.parseDouble(data)
        self.errsPSP = self.parseInt(data)
        self.errsLine = self.parseInt(data)
        self.errsBSHV = self.parseInt(data)
        for i in range(3):
            self.chMask.append(self.parseDWORD(data) > 0)
        self.isCanContinueWork = self.parseDWORD(data) > 0
        self.errorText = self.parseString(data, 256)
        self.priborNomerCode = self.parseDWORD(data)
        self.dupErrorScansN = self.parseDWORD(data)
        self.tachtIRCode = self.parseDouble(data)
        self.startDelay = self.parseInt(data)
