/*
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

   HPSM Algorithm implementation for SCANOSS.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define MAX_LONG_LINE_CHARS 1000
uint8_t crc8_update(uint8_t crc, uint8_t data) {
	uint8_t i;

	crc = crc ^ data;

	for (i = 0; i < 8; ++i) {
		if (crc & 0x01) {
			crc = (crc >> 1) ^ 0x8c;
		} else {
			crc >>= 1;
		}
	}

	return crc;
}


/* Normalize the line
* It will remove any character that is not a letter or a
* number, including spaces, line feeds, and tabs.
*/
static char * normalize(const char *line) 
{
    size_t len = strlen(line);
    char *out = malloc(len + 1);
    size_t outIndex = 0;

    for (size_t i = 0; i < len; i++) {
        char c = line[i];
        if ((c >= '0' && c <= '9') || (c >= 'a' && c <= 'z')) {
            out[outIndex++] = c;
        } else if (c >= 'A' && c <= 'Z') {
            out[outIndex++] = c - 'A' + 'a';
        }
    }

    out[outIndex] = '\0';
    return out;
}

// Hashes a line using CRC-8
static uint8_t get_line_crc8(const char *line) 
{
    size_t len = strlen(line);
    uint8_t checksum = 0;

    for (size_t i = 0; i < len; i++) 
    {
        uint8_t c = line[i];
        checksum = crc8_update(checksum, c);
    }

    return checksum;
}


/* 
* Hashes content
* Calculates CRC-8 of each line contained in a source code string
*/
static uint8_t *get_content_hashes(const char *src, size_t *len) {
    uint8_t *srcChk = NULL;
    size_t size = 0;
    const char *line = src;

    while (*line != '\0') {
        size_t lineLen = strcspn(line, "\n");
        uint8_t checksum = 0;
         if (lineLen == 0) 
        {
            checksum = 0xff;
        }
        else
        {
            char cpy[MAX_LONG_LINE_CHARS] = "\0";
            strncpy(cpy, line, lineLen >= MAX_LONG_LINE_CHARS ? MAX_LONG_LINE_CHARS : lineLen);
            char *normalizedLine = normalize(cpy);
            checksum = get_line_crc8(normalizedLine);
            free(normalizedLine);
        }

        srcChk = realloc(srcChk, (size + 1) * sizeof(uint8_t));
        srcChk[size] = checksum;
        size++;

        line += lineLen + 1;
    }

    *len = size;
    return srcChk;
}

static PyObject* winnowing_compute_hpsm(PyObject* self, PyObject* args) {
    Py_buffer in;
    PyObject* result = PyList_New(0);
    
    if (!PyArg_ParseTuple(args, "y*", &in))
        return NULL;
    const char* content = in.buf;
    size_t size = 0;
    uint8_t *hashes = get_content_hashes(content, &size);
    if (!hashes)
        return NULL;

    for (int i = 0; i < size; i++)
    {
        char crc_s[3];
        snprintf(crc_s, 3, "%02x", hashes[i]);
        PyObject* out_buf = PyByteArray_FromStringAndSize(crc_s, 2); //avoid the null char at the end
        if (PyList_Append(result, out_buf) == -1) {
            free(hashes);
            Py_DECREF(out_buf);
            Py_DECREF(result);
            PyBuffer_Release(&in);
            return NULL;
        }
        Py_DECREF(out_buf);
    }
    free(hashes);
    PyBuffer_Release(&in);
    return result;
}


static PyMethodDef hpsmMethods[] = {
    { "compute_hpsm",
        winnowing_compute_hpsm,
        METH_VARARGS,
        "Compute HPSM crc8 finger print for scanoss." },
    { NULL, NULL, 0, NULL } /* Sentinel */
};

static struct PyModuleDef hpsmmodule = {
    PyModuleDef_HEAD_INIT,
    "_hpsmmodule", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1, /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    hpsmMethods
};

PyObject* PyInit__hpsm(void)
{
    return PyModule_Create(&hpsmmodule);
}
/* C TEST
* To build run: gcc src/scanoss_winnowing/_hpsm.c -o test -I/usr/include/python3.9 -lpython3.9
*/
int main() {
    char *content = "line1\n\nline2\n\n\nline3\n";
    uint8_t expected[] = {0x27, 0xff, 0xc5, 0xff, 0xff, 0x9b};
    size_t size = 0;
    uint8_t *hashes = get_content_hashes(content, &size);
    if (sizeof(expected) == size)
    {
        for (int i = 0; i < size; i++)
        {
            printf("hash %i: %02x - expected: %02x\n", i, hashes[i], expected[i]);
            if (hashes[i] != expected[i])
            {
                printf("Test fail: hash does not match\n");
                exit(EXIT_FAILURE);
            }
        }
    }
    else
    {
        printf("Test fail: hash quantity does not match\n");
        exit(EXIT_FAILURE);
    }

    printf("Test passed\n");
    exit(EXIT_SUCCESS);
    free(hashes);

    return 0;
}

