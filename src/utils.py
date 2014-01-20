import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    #filemode='w',
    #filename='/tmp/dup_find.log',
    datefmt='%a, %d %b %Y %H:%M:%S')
LOG = logging


def size_renderer(size):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    value = size * 10
    min_size = 10240
    while value > min_size:
        i = i + 1
        value = value / 1024
    return "{0} {1}".format(str(round(value / 10, 1)), units[i])
