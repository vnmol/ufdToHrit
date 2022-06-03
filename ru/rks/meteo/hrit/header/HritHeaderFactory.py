from ru.rks.meteo.hrit.header.HritHeader import PRIMARY_HEADER, IMAGE_STRUCTURE, IMAGE_NAVIGATION, IMAGE_DATA_FUNCTION, \
    ANNOTATION, TIME_STAMP, ANCILLARY_TEXT, IMAGE_SEGMENT_LINE_QUALITY, SEGMENT_IDENTIFICATION, KEY_HEADER
from ru.rks.meteo.hrit.header.HritHeaderAncillaryText import HritHeaderAncillaryText
from ru.rks.meteo.hrit.header.HritHeaderAnnotation import HritHeaderAnnotation
from ru.rks.meteo.hrit.header.HritHeaderImageDataFunction import HritHeaderImageDataFunction
from ru.rks.meteo.hrit.header.HritHeaderImageNavigation import HritHeaderImageNavigation
from ru.rks.meteo.hrit.header.HritHeaderImageSegmentLineQuality import HritHeaderImageSegmentLineQuality
from ru.rks.meteo.hrit.header.HritHeaderImageStructure import HritHeaderImageStructure
from ru.rks.meteo.hrit.header.HritHeaderKeyHeader import HritHeaderKeyHeader
from ru.rks.meteo.hrit.header.HritHeaderPrimary import HritHeaderPrimary
from ru.rks.meteo.hrit.header.HritHeaderSegmentIdentification import HritHeaderSegmentIdentification
from ru.rks.meteo.hrit.header.HritHeaderTimeStamp import HritHeaderTimeStamp


def getHeader(headerType):
    if headerType == PRIMARY_HEADER:
        return HritHeaderPrimary()
    elif headerType == IMAGE_STRUCTURE:
        return HritHeaderImageStructure()
    elif headerType == IMAGE_NAVIGATION:
        return HritHeaderImageNavigation()
    elif headerType == IMAGE_DATA_FUNCTION:
        return HritHeaderImageDataFunction()
    elif headerType == ANNOTATION:
        return HritHeaderAnnotation()
    elif headerType == TIME_STAMP:
        return HritHeaderTimeStamp()
    elif headerType == ANCILLARY_TEXT:
        return HritHeaderAncillaryText()
    elif headerType == KEY_HEADER:
        return HritHeaderKeyHeader()
    elif headerType == SEGMENT_IDENTIFICATION:
        return HritHeaderSegmentIdentification()
    elif headerType == IMAGE_SEGMENT_LINE_QUALITY:
        return HritHeaderImageSegmentLineQuality()
