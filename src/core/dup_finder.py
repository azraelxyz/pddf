import os
import csv
import io
import codecs

import utils
from core.file import File
from utils import LOG


class DupFinder:
    def __init__(self, path_list, filter_list):
        self.path_list = path_list
        self.filter_list = filter_list

    def find(self):
        LOG.info("%s walk start", self.__class__.__name__)
        for path in self.path_list:
            file_instances = self.__walk(path)
        LOG.info("%s walk end", self.__class__.__name__)
        prev_filter = self.filter_list[0]
        prev_filter.set_files(file_instances)
        prev_filter.find()
        for _filter in self.filter_list[1:]:
            _filter.set_files(prev_filter.filtered_files)
            _filter.find()
            prev_filter = _filter

    def __walk(self, path):
        file_instances = list()
        for (root, dirs, files) in os.walk(path):
#            LOG.debug("{0} {1} {2}".format(root, dirs, files))
            for _file in files:
                filepath = os.path.join(root, _file)
                if os.path.exists(filepath):
                    file_instance = File(filepath)
                    file_instances.append(file_instance)
        return file_instances

    def dump2file(self, output_file):
        LOG.debug("%s dump2file", self.__class__.__name__)
        with open(output_file, 'w') as fp:
            for files in self.sorted_dup_files:
                fp.write("================\n")
                for _file in files:
                    size = utils.size_renderer(_file.size)
                    fp.write("Size: {0}, File: {1}\n".format(size, _file.path))

    def dump2csv(self, output_csv):
        LOG.debug("%s dump2csv", self.__class__.__name__)
        rows = list()
        for files in self.sorted_dup_files:
            data = [utils.size_renderer(files[0].size)]
            #data.append(files[0].size)
            data.extend([_file.path for _file in files])
            rows.append(data)
        with open(output_csv, 'wb') as f:
            writer = UnicodeCSVWriter(f)
            writer.writerows(rows)

    def dup_files(self):
        return self.filter_list[-1].dup_files

    @property
    def sorted_dup_files(self, reverse=True):
        df = self.filter_list[-1].dup_files
        sort_files = sorted(df, key=lambda _files: _files[0].size,
                            reverse=reverse)
        return sort_files

    @property
    def character_table(self):
        return self.filter_list[-1].char_table

    @property
    def dup_size(self):
        total_size = 0
        for _file in self.filter_list[-1].filtered_files:
            total_size = total_size + _file.size
        return total_size


class UnicodeCSVWriter:
    """
    Python 3 version CSV Writer
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        try:
            # python 2.7
            import StringIO
            self.queue = StringIO.StringIO()
        except:
            # python 3
            self.queue = io.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        try:
            # python 3
            self.writer.writerow([s for s in row])
        except TypeError:
            # python 2.7
            import StringIO
            self.queue = StringIO.StringIO()
            unicode_row = [unicode(str(s).encode("utf-8")) for s in row]
            self.writer.writerow(unicode_row)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        # ... and reencode it into the target encoding
        try:
            # python 3
            data = self.encoder.encode(data)
        except UnicodeDecodeError:
            # python 2.7
            data = data.decode("utf-8")
            data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
