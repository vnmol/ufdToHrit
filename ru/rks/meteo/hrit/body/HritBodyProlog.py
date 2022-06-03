import numpy

from ru.rks.meteo.Assist import FileRW
from ru.rks.meteo.Assist.MeteoAssist import BITS_PER_BYTE
from ru.rks.meteo.hrit.HritRecord import HritRecord
from ru.rks.meteo.hrit.body.HritBody import HritBody, PROLOG
from ru.rks.meteo.hrit.body.tag.HritTagImageAcquisition import HritTagImageAcquisition
from ru.rks.meteo.hrit.body.tag.HritTagImageCalibration import HritTagImageCalibration
from ru.rks.meteo.hrit.body.tag.HritTagSatelliteStatus import HritTagSatelliteStatus
from ru.rks.meteo.hrit.header.HritHeader import PRIMARY_HEADER, ANNOTATION
from ru.rks.meteo.hrit.header.HritHeaderAnnotation import HritHeaderAnnotation
from ru.rks.meteo.hrit.header.HritHeaderPrimary import HritHeaderPrimary


class HritBodyProlog(HritBody):

    def __init__(self):
        super(HritBodyProlog, self).__init__()
        self.status = None
        self.acquisition = None
        self.calibration = None
        self.size = 0

    def getSize(self):
        return self.size

    @staticmethod
    def convertProlog(dest, ufd, imageCalibration, imageAcquisitions, resolution):
        hrit = HritRecord()
        body = HritBodyProlog()
        body.convertFromUfd(ufd, imageCalibration, imageAcquisitions)
        hrit.body = body
        hrit.headers[PRIMARY_HEADER] = HritHeaderPrimary.convertFromUfd(PROLOG)
        hrit.headers[ANNOTATION] = HritHeaderAnnotation.convertFromUfd(PROLOG, ufd, resolution, 0)
        FileRW.write(dest + hrit.headers[ANNOTATION].getString(), hrit.encode())

    def convertFromUfd(self, ufd, imageCalibration, imageAcquisitions):
        self.status = HritTagSatelliteStatus.convertFromUfd(ufd)
        self.acquisition = HritTagImageAcquisition.convertFromUfd(imageAcquisitions)
        self.calibration = HritTagImageCalibration.convertFromUfd(imageCalibration)

    def encode(self):
        buf = []
        buf.append(self.status.encode())
        buf.append(self.acquisition.encode())
        buf.append(self.calibration.encode())
        res = numpy.concatenate(buf)
        self.size = len(res) * BITS_PER_BYTE
        return res


    def decode(self, data, pos):
        self.status = HritTagSatelliteStatus()
        self.acquisition = HritTagImageAcquisition()
        self.calibration = HritTagImageCalibration()
        pos = self.status.decode(data, pos)
        pos = self.acquisition.decode(data, pos)
        pos = self.calibration.decode(data, pos)
        return pos
