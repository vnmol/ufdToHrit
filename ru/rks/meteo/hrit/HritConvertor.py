from ru.rks.meteo.Assist.FileRW import read
from ru.rks.meteo.Assist.MeteoAssist import CHANNEL_COUNT, BYTE_SIZE, WORD_SIZE
from ru.rks.meteo.hrit.HritRecord import HritRecord
from ru.rks.meteo.hrit.body.HritBody import PROLOG, EPILOG, CHANNEL
from ru.rks.meteo.hrit.body.HritBodyChannel import HritBodyChannel
from ru.rks.meteo.hrit.body.HritBodyEpilog import HritBodyEpilog
from ru.rks.meteo.hrit.body.HritBodyProlog import HritBodyProlog
from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.hrit.header import HritHeaderFactory
from ru.rks.meteo.hrit.header.HritHeader import PRIMARY_HEADER, IMAGE_STRUCTURE
from ru.rks.meteo.ufd.UfdDecoder import UfdDecoder, UFD_TAG_RadiometricProcessing, UFD_TAG_ImageAcquisition
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_GeometricProcessing


class HritConvertor:

    def __init__(self):
        self.pos = 0

    @staticmethod
    def convertFromUfd(path, name, dest):
        decoder = UfdDecoder()
        imageCalibration = []
        imageAcquisitions = []
        res = []
        radiometrics = []
        geometrics = []
        ufd = None
        for i in range(CHANNEL_COUNT):
            ufd = decoder.decode(read(path + name + "." + str(i + 1) + ".L15"))
            print()
            print(ufd)
            HritBodyChannel.convertChannel(dest, ufd, i)
            imageCalibration.append(ufd.tags[UFD_TAG_RadiometricProcessing].graduirovkaEasy)
            imageAcquisitions.append(ufd.tags[UFD_TAG_ImageAcquisition])
            res.append(ufd.getResolution())
            radiometrics.append(ufd.tags[UFD_TAG_RadiometricProcessing])
            geometrics.append(ufd.tags[UFD_TAG_GeometricProcessing])
        resolution = "1" if res[0] == 1 and res[1] == 1 and res[2] == 1 else "4"
        HritBodyProlog.convertProlog(dest, ufd, imageCalibration, imageAcquisitions, resolution)
        HritBodyEpilog.convertEpilog(dest, ufd, radiometrics, geometrics, resolution)

    def decode(self, data):
        self.pos = 0
        hrit = HritRecord()
        self.decodeHeaders(data, hrit)
        hrit.body = None
        ftc = hrit.headers[PRIMARY_HEADER].file_type_code
        if ftc == PROLOG:
            hrit.body = HritBodyProlog()
        elif ftc == EPILOG:
            hrit.body = HritBodyEpilog()
        elif ftc == CHANNEL:
            header = hrit.headers[IMAGE_STRUCTURE]
            hrit.body = HritBodyChannel(header.nb, header.nc)
        if hrit.body is None:
            return
        hrit.body.decode(data[self.pos:])
        return hrit

    def decodeHeaders(self, data, hrit):
        self.getHeader(data, hrit)
        while hrit.headers[PRIMARY_HEADER].total_header_length - self.pos >= 3:
            self.getHeader(data, hrit)

    def getHeader(self, data, hrit):
        headerType = HritTag.decodeByte(data[self.pos:self.pos + 1])
        self.pos += BYTE_SIZE
        hh = HritHeaderFactory.getHeader(headerType)
        length = HritTag.decodeWORD(data[self.pos:self.pos + WORD_SIZE]) - 3
        self.pos += WORD_SIZE
        hh.decode(data[self.pos:self.pos + length])
        self.pos += length
        hrit.headers[headerType] = hh
