import numpy

from ru.rks.meteo.Assist import FileRW
from ru.rks.meteo.Assist.MeteoAssist import BITS_PER_BYTE
from ru.rks.meteo.hrit.HritRecord import HritRecord
from ru.rks.meteo.hrit.body.HritBody import HritBody, EPILOG
from ru.rks.meteo.hrit.body.tag.HritTagGeometricProcessing import HritTagGeometricProcessing
from ru.rks.meteo.hrit.body.tag.HritTagRadiometricProcessing import HritTagRadiometricProcessing
from ru.rks.meteo.hrit.header.HritHeader import PRIMARY_HEADER, ANNOTATION
from ru.rks.meteo.hrit.header.HritHeaderAnnotation import HritHeaderAnnotation
from ru.rks.meteo.hrit.header.HritHeaderPrimary import HritHeaderPrimary


class HritBodyEpilog(HritBody):

    def __init__(self):
        super(HritBodyEpilog, self).__init__()
        self.radiometrics = None
        self.geometrics = None
        self.size = 0

    def getSize(self):
        return self.size

    @staticmethod
    def convertEpilog(dest, ufd, radiometrics, geometrics, resolution):
        hrit = HritRecord()
        body = HritBodyEpilog()
        body.convertFromUfd(radiometrics, geometrics)
        hrit.body = body
        hrit.headers[PRIMARY_HEADER] = HritHeaderPrimary.convertFromUfd(EPILOG)
        hrit.headers[ANNOTATION] = HritHeaderAnnotation.convertFromUfd(EPILOG, ufd, resolution, 0)
        FileRW.write(dest + hrit.headers[ANNOTATION].getString(), hrit.encode())

    def convertFromUfd(self, radiometrics, geometrics):
        self.radiometrics = HritTagRadiometricProcessing.convertFromUfd(radiometrics)
        self.geometrics = HritTagGeometricProcessing.convertFromUfd(geometrics)


    def encode(self):
        buf = []
        buf.append(self.radiometrics.encode())
        buf.append(self.geometrics.encode())
        res = numpy.concatenate(buf)
        self.size = len(res) * BITS_PER_BYTE
        return res

    def decode(self, data, pos):
        self.radiometrics = HritTagRadiometricProcessing()
        self.geometrics = HritTagGeometricProcessing()
        pos = self.radiometrics.decode(data, pos)
        pos = self.geometrics.decode(data, pos)
        return pos
