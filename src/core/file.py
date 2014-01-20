import hashlib
import os

import setting
from utils import LOG

NUM_BLOCKS = 16
NUM_CHUNKS = 4


class File:
    def __init__(self, filepath):
        self.filepath = filepath

    @property
    def md5sum(self):
        ret = setting.UNKNOWN_SYMBOL
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
        ret = setting.UNKNOWN_SYMBOL
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
