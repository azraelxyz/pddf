import os
import sys
import time


import utils
import core.algorithm
import core.dup_finder
from utils import LOG
from core.file import File

# for python 2.7
# reload(sys)
# sys.setdefaultencoding("UTF-8")


def main():
    path = sys.argv[1]
    LOG.info("Start to find duplicated files on {0}".format(path))

    if os.path.isfile(path):
        start_time = time.time()
        print (File(path).md5sum)
        end_time = time.time()
        print (end_time - start_time)
    else:
        start_time = time.time()
        algorithm = core.algorithm.HybridQuick()
        dup_finder = core.dup_finder.DupFinder([path], algorithm)
        dup_finder.find()
        end_time = time.time()
        dup_finder.dump2csv()
        print (end_time - start_time)
        print (utils.size_renderer(dup_finder.dup_size))


if __name__ == '__main__':
    exit(main())
