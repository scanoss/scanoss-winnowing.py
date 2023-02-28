"""
 SPDX-License-Identifier: MIT

   Copyright (c) 2023, SCANOSS

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
"""
import os
import unittest
import time

from scanoss_winnowing.winnowing import Winnowing


class MyTestCase(unittest.TestCase):
    maxDiff = None

    def test_winnowing(self):
        winnowing = Winnowing(debug=True)
        filename = "test-file.c"
        contents = "c code contents"
        content_types = bytes(contents, encoding="raw_unicode_escape")
        wfp = winnowing.wfp_for_contents(filename, False, content_types)
        print(f'WFP for {filename}: {wfp}')
        self.assertIsNotNone(wfp)
        filename = __file__
        wfp = winnowing.wfp_for_file(filename, filename)
        print(f'WFP for {filename}: {wfp}')
        self.assertIsNotNone(wfp)

    def test_winnowing_c(self):
        winnowing = Winnowing(debug=True, c_accelerated=True)
        filename = "test-file.py"
        with open(__file__, 'rb') as f:
            contents = f.read()
        wfp = winnowing.wfp_for_contents(filename, False, contents)

        winnowing = Winnowing(debug=True, c_accelerated=False)
        wfp_expected = winnowing.wfp_for_contents(filename, False, contents)
        self.assertEqual(wfp, wfp_expected)

    def test_winnowing_size_limit(self):
        winnowing = Winnowing(debug=True, c_accelerated=True, post_size=2)
        filename = "../src/scanoss_winnowing/winnowing.py"
        if not os.path.exists(filename) or not os.path.isfile(filename):
            filename = "src/scanoss_winnowing/winnowing.py"
            if not os.path.exists(filename) or not os.path.isfile(filename):
                self.fail(f'Test file does not exist: {filename}')
        with open(filename, 'rb') as f:
            contents = f.read()
        wfp = winnowing.wfp_for_contents(filename, False, contents)

        winnowing = Winnowing(debug=True, c_accelerated=False, post_size=2)
        wfp_expected = winnowing.wfp_for_contents(filename, False, contents)
        self.assertEqual(wfp, wfp_expected)

    def test_winnowing_timings(self):
        winnowing = Winnowing(debug=True, c_accelerated=True)
        filename = "test-file.py"
        with open(__file__, 'rb') as f:
            contents = f.read()
        t1 = time.time()
        for i in range(1000):
            wfp = winnowing.wfp_for_contents(filename, False, contents)
        t2 = time.time()
        x1 = t2 - t1
        winnowing = Winnowing(debug=True, c_accelerated=False)
        t1 = time.time()
        for i in range(100):
            wfp_expected = winnowing.wfp_for_contents(filename, False, contents)
        t2 = time.time()
        x2 = t2 - t1
        print(x1, x2, 10 * x2 / x1)
        self.assertEqual(wfp, wfp_expected)

    def test_snippet_skip(self):
        winnowing = Winnowing(debug=True)
        filename = "test-file.jar"
        contents = "jar file contents"
        content_types = bytes(contents, encoding="raw_unicode_escape")
        wfp = winnowing.wfp_for_contents(filename, False, content_types)
        print(f'WFP for {filename}: {wfp}')
        self.assertIsNotNone(wfp)

    def test_normalize(self):
        res = bytes([Winnowing._normalize(i) for i in range(255)])
        exp = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
              b'\x000123456789\x00\x00\x00\x00\x00\x00\x00abcdefghijklmnopqrstuvwxyz\x00\x00\x00\x00\x00' \
              b'\x00abcdefghijklmnopqrstuvwxyz\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.assertEqual(res, exp)


if __name__ == '__main__':
    unittest.main()
