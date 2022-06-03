import sys


from ru.rks.meteo.hrit.HritConvertor import HritConvertor


if __name__ == '__main__':
    #HritConvertor.convertFromUfd(sys.argv[1], sys.argv[2], sys.argv[3])
    HritConvertor.convertFromUfd('/home/mol/UFD_HRIT/source/',
                                 'EL2 - 2021 05 08 - 14 00 00 - 20210508-140001',
                                 '/home/mol/UFD_HRIT/dest/')
