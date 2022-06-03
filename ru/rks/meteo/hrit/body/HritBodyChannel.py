import numpy as np
import dask.array as da
from numpy import uint8, uint16

from ru.rks.meteo.Assist import FileRW
from ru.rks.meteo.Assist.MeteoAssist import SECTION_SIZE, HIGH_BITS_PER_PIX, LOW_BITS_PER_PIX
from ru.rks.meteo.hrit.HritRecord import HritRecord
from ru.rks.meteo.hrit.body.HritBody import HritBody, CHANNEL
from ru.rks.meteo.hrit.header.HritHeader import ANNOTATION, IMAGE_NAVIGATION, SEGMENT_IDENTIFICATION
from ru.rks.meteo.hrit.header.HritHeaderAnnotation import HritHeaderAnnotation
from ru.rks.meteo.hrit.header.HritHeaderFactory import PRIMARY_HEADER, IMAGE_STRUCTURE
from ru.rks.meteo.hrit.header.HritHeaderImageNavigation import HritHeaderImageNavigation
from ru.rks.meteo.hrit.header.HritHeaderImageStructure import HritHeaderImageStructure
from ru.rks.meteo.hrit.header.HritHeaderPrimary import HritHeaderPrimary
from ru.rks.meteo.hrit.header.HritHeaderSegmentIdentification import HritHeaderSegmentIdentification
from ru.rks.meteo.ufd.UfdRecord import UFD_TAG_Image


class HritBodyChannel(HritBody):

    def __init__(self, bits_per_pixel, width):
        super(HritBodyChannel, self).__init__()
        self.bits_per_pixel = bits_per_pixel
        self.width = width
        self.data = None

    def getSize(self):
        return SECTION_SIZE * self.width * self.bits_per_pixel

    @staticmethod
    def convertChannel(dest, ufd, channelID):
        tag = ufd.tags[UFD_TAG_Image]
        segment_count = tag.spkInfo_Height // SECTION_SIZE
        for segment in range(segment_count):
            hrit = HritRecord()
            bpp = HIGH_BITS_PER_PIX if tag.spkInfo_BitPerPix >= 10 else LOW_BITS_PER_PIX
            body = HritBodyChannel(bpp, tag.spkInfo_Width)
            body.convertFromUfd(ufd, segment)
            hrit.body = body
            hrit.headers[PRIMARY_HEADER] = HritHeaderPrimary.convertFromUfd(CHANNEL)
            hrit.headers[IMAGE_STRUCTURE] = HritHeaderImageStructure.convertFromUfd(ufd)
            hrit.headers[IMAGE_NAVIGATION] = HritHeaderImageNavigation.convertFromUfd(ufd)
            hrit.headers[ANNOTATION] = HritHeaderAnnotation.convertFromUfd(CHANNEL, ufd, '', segment)
            hrit.headers[SEGMENT_IDENTIFICATION] = \
                HritHeaderSegmentIdentification.convertFromUfd(ufd, channelID, segment, segment_count)
            if segment == 0:
                print(hrit)
            res = hrit.encode()
            FileRW.write(dest + hrit.headers[ANNOTATION].getString(), res)

    def convertFromUfd(self, ufd, segment):
        tag = ufd.tags[UFD_TAG_Image]
        shift = tag.spkInfo_BitPerPix - self.bits_per_pixel
        isShiftToTheRight = True
        if shift < 0:
            shift = -shift
            isShiftToTheRight = False
        self.data = tag.data[SECTION_SIZE * segment:SECTION_SIZE * (segment + 1), 0:self.width]
        self.data = self.data >> shift if isShiftToTheRight else self.data << shift

    def decode(self, data):
        data16 = data.astype(uint16)
        data_0 = data16[0::5]
        data_1 = data16[1::5]
        data_2 = data16[2::5]
        data_3 = data16[3::5]
        data_4 = data16[4::5]
        res_0 = (data_0 << 2) + (data_1 >> 6)
        res_1 = ((data_1 & 63) << 4) + (data_2 >> 4)
        res_2 = ((data_2 & 15) << 6) + (data_3 >> 2)
        res_3 = ((data_3 & 3) << 8) + data_4
        res = da.stack([res_0, res_1, res_2, res_3], axis=-1).__array__().reshape(SECTION_SIZE, self.width)
        return res

    def encode(self):
        data = self.data.reshape(np.size(self.data))
        data_0 = data[0::4]
        data_1 = data[1::4]
        data_2 = data[2::4]
        data_3 = data[3::4]
        res_0 = data_0 >> 2
        res_1 = ((data_0 & 3) << 6) + (data_1 >> 4)
        res_2 = ((data_1 & 15) << 4) + (data_2 >> 6)
        res_3 = ((data_2 & 63) << 2) + (data_3 >> 8)
        res_4 = data_3 & 255
        res = da.stack([res_0, res_1, res_2, res_3, res_4], axis=-1).astype(dtype=uint8).ravel().__array__()
        return res

    def test_encode(self):
        self.data = np.array([(0, 1, 2, 3, 4, 5, 6, 7),
                              (10, 11, 12, 13, 14, 15, 16, 17),
                              (20, 21, 22, 23, 24, 25, 26, 27)], dtype=np.uint16)
        print(self.data)
        res = self.encode()
        print(self.decode(res))


if __name__ == '__main__':
    SECTION_SIZE = 3
    HritBodyChannel(10, 8).test_encode()
