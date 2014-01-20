import os
import hashlib
import sys
import time
import logging
import csv
import io
import codecs
try:
    import StringIO
except:
    import io as StringIO

# for python 2.7
# reload(sys)
# sys.setdefaultencoding("UTF-8")

NUM_BLOCKS = 16
NUM_CHUNKS = 4
UNKNOWN_SYMBOL = "--"

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    #filemode='w',
    #filename='/tmp/dup_find.log',
    datefmt='%a, %d %b %Y %H:%M:%S')
LOG = logging


class File:
    def __init__(self, filepath):
        self.filepath = filepath

    @property
    def md5sum(self):
        ret = UNKNOWN_SYMBOL
        try:
            with open(self.filepath, 'rb') as fp:
                chunk_size = 1024 * hashlib.md5().block_size
                chksum = hashlib.md5()
                while True:
                    chunk = fp.read(chunk_size)
                    if chunk:
                        chksum.update(chunk)
                    else:
                        break
            ret = chksum.hexdigest()
        except Exception as e:
            LOG.error("Get {0}'s md5sum error".format(self.path))
            LOG.exception(e)
        return ret

    @property
    def slow_md5sum(self):
        return hashlib.md5(open(self.filepath).read()).hexdigest()

    @property
    def character(self):
        chunks = list()
        size = self.size
        ret = UNKNOWN_SYMBOL
        try:
            with open(self.filepath, 'rb') as f:
                for i in range(NUM_CHUNKS):
                    f.seek(int(size / NUM_CHUNKS) * i)
                    chunk = f.read(NUM_BLOCKS * hashlib.md5().block_size)
                    chunks.append(chunk)
            character_chunk = bytes()
            for chunk in chunks:
                character_chunk = character_chunk + chunk
            ret = hashlib.md5(character_chunk).hexdigest()
        except Exception as e:
            LOG.error("Get {0}'s character error".format(self.path))
            LOG.exception(e)
        return ret

    @property
    def path(self):
        return self.filepath

    @property
    def size(self):
        size = 0
        try:
            size = os.path.getsize(self.filepath)
        except Exception as e:
            LOG.error("Get {0}'s size error".format(self.path))
            LOG.exception(e)
        return size


class AbstractAlgorithm:
    def __init__(self):
        self.char_table = dict()
        self.files = list()

    def set_files(self, files):
        self.files = files

    def find(self):
        raise Exception('find not implement')

    @property
    def dup_files(self):
        ret = list()
        for k, v in self.char_table.items():
            LOG.debug("{0} {1}".format(k, v))
            LOG.debug(k)
            if len(v) > 1:
                ret.append(v)
        return ret

    @property
    def filtered_files(self):
        ret = list()
        for k, v in self.char_table.items():
            LOG.debug("{0} {1}".format(k, v))
            if len(v) > 1:
                ret.extend(v)
        return ret


class FullScanner(AbstractAlgorithm):
    def find(self):
        for _file in self.files:
            md5sum = _file.md5sum
            if md5sum == UNKNOWN_SYMBOL:
                continue
            entry = self.char_table.get(md5sum)
            if entry:
                entry.append(_file)
            else:
                self.char_table[md5sum] = [_file]


class SizeChecker(AbstractAlgorithm):
    def find(self):
        for _file in self.files:
            character = _file.size
            entry = self.char_table.get(character)
            if entry:
                entry.append(_file)
            else:
                self.char_table[character] = [_file]


class CharacterScanner(AbstractAlgorithm):
    def find(self):
        for _file in self.files:
            character = _file.character
            if character == UNKNOWN_SYMBOL:
                continue
            entry = self.char_table.get(character)
            if entry:
                entry.append(_file)
            else:
                self.char_table[character] = [_file]


class HybridQuick(AbstractAlgorithm):
    def find(self):
        size_checker = SizeChecker()
        size_checker.set_files(self.files)
        size_checker.find()
        character_scanner = CharacterScanner()
        character_scanner.set_files(size_checker.filtered_files)
        character_scanner.find()
        self.char_table = character_scanner.char_table


class HybridFull(AbstractAlgorithm):
    def find(self):
        size_checker = SizeChecker()
        size_checker.set_files(self.files)
        size_checker.find()
        character_scanner = CharacterScanner()
        character_scanner.set_files(size_checker.filtered_files)
        character_scanner.find()
        full_scanner = FullScanner()
        full_scanner.set_files(character_scanner.filtered_files)
        full_scanner.find()
        self.char_table = full_scanner.char_table


class DupFinder:
    def __init__(self, path, algorithm):
        self.path = path
        self.algorithm = algorithm

    def find(self):
        file_instances = list()
        for (root, dirs, files) in os.walk(self.path):
            LOG.debug("{0} {1} {2}".format(root, dirs, files))
            for _file in files:
                filepath = os.path.join(root, _file)
                if os.path.exists(filepath):
                    file_instance = File(filepath)
                    file_instances.append(file_instance)
        self.algorithm.set_files(file_instances)
        self.algorithm.find()

    def dump2file(self):
        output_file = 'output.txt'
        with open(output_file, 'w') as fp:
            for files in self.dup_files:
                fp.write("================\n")
                for _file in files:
                    size = size_renderer(_file.size)
                    fp.write("Size: {0}, File: {1}\n".format(size, _file.path))

    def dump2csv(self):
        output_file = 'output.csv'
        rows = list()
        for files in self.dup_files:
            data = [size_renderer(files[0].size)]
            data.append(files[0].size)
            data.extend([_file.path for _file in files])
            rows.append(data)
#            rows = list()
#            row = ['a1', 'b1', 'c1']
#            rows.append(row)
#            row = ['a2', 'b2', 'c2']
#            rows.append(row)
        with open(output_file, 'wb') as f:
            writer = Py3UnicodeWriter(f)
            writer.writerows(rows)

    @property
    def dup_files(self):
        return self.algorithm.dup_files

    @property
    def character_table(self):
        return self.algorithm.char_table

    @property
    def dup_size(self):
        total_size = 0
        for _file in self.algorithm.filtered_files:
            total_size = total_size + _file.size
        return total_size


class Py3UnicodeWriter:
    """
    Python 3 version CSV Writer
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = io.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class Py2UnicodeWriter:
    """
    Python 2 version CSV Writer
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def size_renderer(size):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    value = size * 10
    min_size = 10240
    while value > min_size:
        i = i + 1
        value = value / 1024
    return "{0} {1}".format(str(value / 10), units[i])


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
        dup_finder = DupFinder(path, HybridQuick())
        dup_finder.find()
        end_time = time.time()
        dup_finder.dump2csv()
        print (end_time - start_time)
        print (size_renderer(dup_finder.dup_size))


if __name__ == '__main__':
    exit(main())
