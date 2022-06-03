import numpy as np

from ru.rks.meteo.hrit.body.tag.HritTag import HritTag
from ru.rks.meteo.hrit.header.HritHeaderFactory import PRIMARY_HEADER


class HritRecord:

    def __init__(self):
        self.headers = {}
        self.body = None

    def encode(self):
        buf = []
        for key in self.headers:
            buf.append(self.headers[key].encode())
        hhp = self.headers[PRIMARY_HEADER]
        hhp.total_header_length = HritTag.getLength(buf)
        body = self.body.encode()
        buf.append(body)
        hhp.data_field_length = self.body.getSize()
        buf[0] = hhp.encode()
        res = np.concatenate(buf)
        return res

    def __str__(self):
        res = type(self).__name__ + '{'
        flag = False
        for item in vars(self).items():
            if flag:
                res += ', '
            else:
                flag = True
            if item[0] == 'body':
                res += '\n'
            res += item[0] + '='
            if isinstance(item[1], dict):
                res += self.dict_str(item[1])
            else:
                res += str(item[1])
        res += '}'
        return res

    def dict_str(self, tags):
        res = '{'
        flag = False
        for indx in tags:
            if flag:
                res += ', '
            else:
                flag = True
            res += '\n' + str(indx) + '=' + str(tags[indx])
        res += '}'
        return res
