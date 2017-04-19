# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import os
import shutil
import unittest

from obspy.core.compatibility import mock
from obspy.core.util.base import NamedTemporaryFile, get_dependency_version
from obspy.core.util.testing import ImageComparison, ImageComparisonException


class UtilBaseTestCase(unittest.TestCase):
    """
    Test suite for obspy.core.util.base
    """
    def test_get_matplotlib_version(self):
        """
        Tests for the get_matplotlib_version() function as it continues to
        cause problems.
        """
        versions = (("1.2.3", [1, 2, 3]), ("0.9.11", [0, 9, 11]),
                    ("0.9.svn", [0, 9, 0]), ("1.1.1~rc1-1", [1, 1, 1]),
                    ("1.2.x", [1, 2, 0]), ("1.3.1rc2", [1, 3, 1]))

        for version_string, expected in versions:
            with mock.patch('pkg_resources.get_distribution') as p:
                class _D(object):
                    version = version_string
                p.return_value = _D()
                got = get_dependency_version('matplotlib')
            self.assertEqual(expected, got)

    def test_named_temporay_file__context_manager(self):
        """
        Tests the automatic closing/deleting of NamedTemporaryFile using the
        context manager.
        """
        content = b"burn after writing"
        # write something to tempfile and check closing/deletion afterwards
        with NamedTemporaryFile() as tf:
            filename = tf.name
            tf.write(content)
        self.assertFalse(os.path.exists(filename))
        # write something to tempfile and check that it is written correctly
        with NamedTemporaryFile() as tf:
            filename = tf.name
            tf.write(content)
            tf.close()
            with open(filename, 'rb') as fh:
                tmp_content = fh.read()
        self.assertEqual(content, tmp_content)
        self.assertFalse(os.path.exists(filename))
        # check that closing/deletion works even when nothing is done with file
        with NamedTemporaryFile() as tf:
            filename = tf.name
        self.assertFalse(os.path.exists(filename))

    def test_image_comparison(self):
        """
        Tests the image comparison mechanism with an expected fail and an
        expected passing test.
        Also tests that temporary files are deleted after both passing and
        failing tests.
        """
        path = os.path.join(os.path.dirname(__file__), "images")
        img_basename = "image.png"
        img_ok = os.path.join(path, "image_ok.png")
        img_fail = os.path.join(path, "image_fail.png")

        # image comparison that should pass
        with ImageComparison(path, img_basename) as ic:
            shutil.copy(img_ok, ic.name)
            self.assertTrue(os.path.exists(ic.name))
        # check that temp file is deleted
        self.assertFalse(os.path.exists(ic.name))

        # image comparison that should raise
        # avoid uploading the staged test fail image
        # (after an estimate of 10000 uploads of it.. ;-))
        with mock.patch.object(ImageComparison, '_upload_images',
                               new=mock.MagicMock(return_value='')):
            with self.assertRaises(ImageComparisonException):
                with ImageComparison(path, img_basename,
                                     adjust_tolerance=False) as ic:
                    shutil.copy(img_fail, ic.name)

        # check that temp file is deleted
        self.assertFalse(os.path.exists(ic.name))


def suite():
    return unittest.makeSuite(UtilBaseTestCase, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
