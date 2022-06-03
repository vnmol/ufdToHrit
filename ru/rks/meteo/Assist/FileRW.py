import numpy


def read(name):
    data = numpy.fromfile(name, dtype='b')
    return data

def write(fileName, data):
    data.tofile(fileName)
