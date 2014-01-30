# coding=utf-8
import unittest
#import StringIO

from mockito import when, verify

import core.algorithm
import core.dup_finder
from core.file import File


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_find(self):
        path = "/home/test/downloads"
        size_filter = core.algorithm.SizeFilter()
        char_filter = core.algorithm.CharacterFilter()
        filters = [
            size_filter,
            char_filter
        ]
        dup_finder = core.dup_finder.DupFinder([path], filters)
        file_a = File("/home/test/downloads/a")
        file_b = File("/home/test/downloads/b")
        file_insts = [file_a, file_b]
        when(core.dup_finder.Walker).walk([path]).thenReturn(file_insts)
        when(size_filter).find().thenReturn(None)
        size_filter.filtered_files = file_insts
        when(size_filter).set_files().thenReturn(None)
        when(char_filter).set_files().thenReturn(None)
        when(char_filter).find().thenReturn(None)
        char_filter.filtered_files = []
        dup_finder.find()
        verify(core.dup_finder.Walker).walk([path])
        verify(size_filter).set_files(file_insts)
        verify(size_filter).find()
        verify(char_filter).set_files(file_insts)
        verify(char_filter).find()
        self.assertEqual([], dup_finder.dup_files)

if __name__ == "__main__":
    unittest.main()
