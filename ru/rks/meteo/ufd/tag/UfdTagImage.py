from datetime import datetime

from numpy import uint16, empty

from ru.rks.meteo.ufd.tag.UfdTag import UfdTag


class UfdTagImage(UfdTag):

    def __init__(self):
        super(UfdTagImage, self).__init__()
        self.tagChGroup = 0
        self.typeImage = 0
        self.attributePresenceInformation = 0
        self.spkInfo_Width = 0
        self.spkInfo_Height = 0
        self.spkInfo_BitPerPix = 0
        self.data = None

    def parse(self, data):
        self.tagChGroup = self.parseDWORD(data)
        self.typeImage = self.parseDWORD(data)
        self.attributePresenceInformation = self.parseDWORD(data)
        self.spkInfo_Width = self.parseDWORD(data)
        self.spkInfo_Height = self.parseDWORD(data)
        self.spkInfo_BitPerPix = self.parseDWORD(data)
        width = self.spkInfo_Width
        height = self.spkInfo_Height
        self.data = data[self.pos:self.pos + height * width * 2].view(uint16).reshape(height, width).copy()
        self.pos += height * width * 2
