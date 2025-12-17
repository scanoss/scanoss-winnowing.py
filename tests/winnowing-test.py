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
        self.assertIsNotNone(wfp)
        filename = __file__
        wfp = winnowing.wfp_for_file(filename, filename)
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
        winnowing = Winnowing(debug=True, c_accelerated=True, post_size=2, size_limit=True)
        filename = "../src/scanoss_winnowing/winnowing.py"
        if not os.path.exists(filename) or not os.path.isfile(filename):
            filename = "src/scanoss_winnowing/winnowing.py"
            if not os.path.exists(filename) or not os.path.isfile(filename):
                self.fail(f'Test file does not exist: {filename}')
        with open(filename, 'rb') as f:
            contents = f.read()
        wfp = winnowing.wfp_for_contents(filename, False, contents)

        winnowing = Winnowing(debug=True, c_accelerated=False, post_size=2, size_limit=True)
        wfp_expected = winnowing.wfp_for_contents(filename, False, contents)
        self.assertEqual(wfp, wfp_expected)

    def test_winnowing_timings(self):
        winnowing = Winnowing(debug=True, c_accelerated=True)
        filename = "test-file.py"
        with open(__file__, 'rb') as f:
            contents = f.read()
        t1 = time.time()
        wfp = ""
        for i in range(1000):
            wfp = winnowing.wfp_for_contents(filename, False, contents)
        t2 = time.time()
        x1 = t2 - t1
        winnowing = Winnowing(debug=True, c_accelerated=False)
        t1 = time.time()
        wfp_expected = ""
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
    
    def test_hpsm_c(self):
        winnowing = Winnowing(debug=True, hpsm=True, c_accelerated=True)
        filename = "test-file.py"
        with open(__file__, 'rb') as f:
            contents = f.read()
        wfp = winnowing.wfp_for_contents(filename, False, contents)

        winnowing = Winnowing(debug=True, hpsm=True, c_accelerated=False)
        wfp_expected = winnowing.wfp_for_contents(filename, False, contents)
        self.assertEqual(wfp, wfp_expected)
     
    def test_snippet_strip(self):
        winnowing = Winnowing(debug=True, hpsm=True, c_accelerated=False,
                              strip_snippet_ids=['d5e54c33,b03faabe'], 
                              strip_hpsm_ids=['f7cffc62d1801413bff9bacfff'])
        filename = "test-file.py"
        with open(__file__, 'rb') as f:
            contents = f.read()
        print('--- Test snippet and HPSM strip ---')
        wfp = winnowing.wfp_for_contents(filename, False, contents)
        found = 0
        print(f'WFP for {filename}: {wfp}')
        try:
            found = wfp.index('d5e54c33,b03faabe')
        except ValueError:
            found = -1
        self.assertEqual(found, -1)       
        
        try:
            found = wfp.index('f7cffc62d1801413bff9bacfff')
        except ValueError:
            found = -1
        self.assertEqual(found, -1)
        
        print('--- Test accelerated mode ---')
        winnowing = Winnowing(debug=True, hpsm=True, c_accelerated=True, 
                              strip_snippet_ids= ['d5e54c33,b03faabe'], 
                              strip_hpsm_ids= ['f7cffc62d1801413bff9bacfff'])
        wfp_acc = winnowing.wfp_for_contents(filename, False, contents)
        self.assertEqual(wfp, wfp_acc)

    def test_skip_headers_flag(self):
        """Test skip_headers flag functionality."""
        # Sample Python file with headers, imports, and implementation
        test_content = b"""# Copyright 2024 SCANOSS
# Licensed under MIT License
# All rights reserved

import os
import sys
import json
from pathlib import Path

def function1():
    data = {"key": "value"}
    return json.dumps(data)

def function2():
    path = Path("/tmp")
    return str(path)

class MyClass:
    def __init__(self):
        self.data = []

    def add_item(self, item):
        self.data.append(item)
"""

        # Test WITHOUT skip_headers
        winnowing_no_skip = Winnowing(debug=False, skip_headers=False)
        wfp_no_skip = winnowing_no_skip.wfp_for_contents('test.py', False, test_content)

        # Test WITH skip_headers
        winnowing_skip = Winnowing(debug=False, skip_headers=True)
        wfp_skip = winnowing_skip.wfp_for_contents('test.py', False, test_content)

        print(f'WFP without skip_headers:\n{wfp_no_skip}')
        print(f'\nWFP with skip_headers:\n{wfp_skip}')

        # Both should have file= line
        self.assertIn('file=', wfp_no_skip)
        self.assertIn('file=', wfp_skip)

        # Extract snippet line numbers from both WFPs
        def extract_line_numbers(wfp):
            lines = wfp.split('\n')
            line_numbers = []
            for line in lines:
                if '=' in line and line.split('=')[0].isdigit():
                    line_numbers.append(int(line.split('=')[0]))
            return line_numbers

        lines_no_skip = extract_line_numbers(wfp_no_skip)
        lines_skip = extract_line_numbers(wfp_skip)

        # Both should have snippet lines
        self.assertGreater(len(lines_no_skip), 0, "Should have snippets without skip_headers")
        self.assertGreater(len(lines_skip), 0, "Should have snippets with skip_headers")

        # First line number with skip_headers should be HIGHER (skipped headers/imports)
        # Line 10 in the content is "def function1():" which is where real code starts
        min_line_no_skip = min(lines_no_skip)
        min_line_skip = min(lines_skip)

        print(f'First snippet line without skip_headers: {min_line_no_skip}')
        print(f'First snippet line with skip_headers: {min_line_skip}')

        # With skip_headers, first line should be after imports (around line 10+)
        # Without skip_headers, first line should be earlier (around line 5-8)
        self.assertGreater(
            min_line_skip,
            min_line_no_skip,
            "skip_headers should result in higher starting line number"
        )

        # Verify line 10+ (implementation) appears in skip_headers output
        self.assertGreaterEqual(
            min_line_skip,
            10,
            "With skip_headers, snippets should start at implementation (line 10+)"
        )

        # Verify start_line tag is present in skip_headers output
        self.assertIn('start_line=', wfp_skip, "start_line tag should be present with skip_headers")
        self.assertNotIn('start_line=', wfp_no_skip, "start_line tag should NOT be present without skip_headers")

        # Extract and validate start_line value
        start_line_value = None
        for line in wfp_skip.split('\n'):
            if line.startswith('start_line='):
                start_line_value = int(line.split('=')[1])
                break

        self.assertIsNotNone(start_line_value, "start_line value should be found")
        self.assertGreater(start_line_value, 0, "start_line should indicate skipped lines")
        print(f'start_line tag value: {start_line_value}')



if __name__ == '__main__':
    unittest.main()
