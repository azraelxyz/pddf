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
        self.progress = 0
        self.step = None
        self.total = None

    def find(self):
        LOG.info("%s walk start", self.__class__.__name__)
        walker = Walker()
        self.__update_step(walker)
        file_instances = walker.walk(self.path_list)
        LOG.info("%s walk end", self.__class__.__name__)
        prev_filter = self.filter_list[0]
        prev_filter.set_files(file_instances)
        self.total = len(file_instances)
        self.__update_step(prev_filter)
        prev_filter.find()
        for _filter in self.filter_list[1:]:
            _filter.set_files(prev_filter.filtered_files)
            self.__update_step(_filter)
            _filter.find()
            prev_filter = _filter

    def __update_step(self, instance):
        self.step = instance

    def get_progress(self):
        return self.step.progress

    def get_total(self):
        return self.total

    def get_step(self):
        step_index = "0"
        try:
            step_index = str(self.filter_list.index(self.step) + 1)
        except ValueError:
            pass
        total_step = len(self.filter_list)
        step_name = self.step.__class__.__name__
        return "Step {0}/{1} {2}".format(step_index, total_step, step_name)

    def dump2file(self, output_file):
        LOG.debug("%s dump2file", self.__class__.__name__)
        if utils.get_python_version() == 3:
            fp = codecs.open(output_file, "w", "utf-8")
        else:
            fp = open(output_file, 'w')
        try:
            for files in self.sorted_dup_files:
                fp.write("================\n")
                for _file in files:
                    size = utils.size_renderer(_file.size)
                    fp.write("Size: {0}, File: {1}\n".format(size, _file.path))
        finally:
            fp.close()

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

    @property
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


class Walker:
    def __init__(self):
        self.progress = 0

    def get_progress(self):
        return self.progress

    def walk(self, path_list):
        file_instances = list()
        for path in path_list:
            file_instances.extend(self.__path_walk(path))
        return file_instances

    def __path_walk(self, path):
        file_instances = list()
        for (root, dirs, files) in os.walk(path):
#            LOG.debug("{0} {1} {2}".format(root, dirs, files))
            for _file in files:
                filepath = os.path.join(root, _file)
                if os.path.exists(filepath):
                    file_instance = File(filepath)
                    file_instances.append(file_instance)
                    self.progress = self.progress + 1
        return file_instances


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
