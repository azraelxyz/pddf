import setting
from utils import LOG


class AbstractFilter:
    def __init__(self):
        self.char_table = dict()
        self.files = list()

    def set_files(self, files):
        LOG.debug("%s set_files", self.__class__.__name__)
        self.files = files

    def find(self):
        raise Exception('find not implement')

    @property
    def dup_files(self):
        LOG.debug("%s dup_files", self.__class__.__name__)
        ret = list()
        for k, v in self.char_table.items():
#            LOG.debug("{0} {1}".format(k, v))
#            LOG.debug(k)
            if len(v) > 1:
                ret.append(v)
        return ret

    @property
    def filtered_files(self):
        LOG.debug("%s filtered_files", self.__class__.__name__)
        ret = list()
        for k, v in self.char_table.items():
            #LOG.debug("{0} {1}".format(k, v))
            if len(v) > 1:
                ret.extend(v)
        return ret


class FullScanner(AbstractFilter):
    def find(self):
        LOG.debug("%s find", self.__class__.__name__)
        for _file in self.files:
            md5sum = _file.md5sum
            if md5sum == setting.UNKNOWN_SYMBOL:
                continue
            entry = self.char_table.get(md5sum)
            if entry:
                entry.append(_file)
            else:
                self.char_table[md5sum] = [_file]


class SizeFilter(AbstractFilter):
    def find(self):
        LOG.debug("%s find", self.__class__.__name__)
        for _file in self.files:
            character = _file.size
            entry = self.char_table.get(character)
            if entry:
                entry.append(_file)
            else:
                self.char_table[character] = [_file]


class CharacterFilter(AbstractFilter):
    def find(self):
        LOG.debug("%s find", self.__class__.__name__)
        for _file in self.files:
            character = _file.character
            if character == setting.UNKNOWN_SYMBOL:
                continue
            entry = self.char_table.get(character)
            if entry:
                entry.append(_file)
            else:
                self.char_table[character] = [_file]
