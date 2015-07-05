# -*- coding: utf-8 -*-
"""
util.py

Created by Stephan Hügel on 2015-06-22

This file is part of convertbng.

The MIT License (MIT)

Copyright (c) 2015 Stephan Hügel

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
from ctypes import cdll, c_uint32, c_float, Structure, c_int32, c_void_p, cast, c_size_t, POINTER
from sys import platform
import os

if platform == "darwin":
    ext = "dylib"
else:
    ext = "so"

__author__ = u"Stephan Hügel"
__version__ = "0.1.17"


# hacky: http://stackoverflow.com/a/30789980/416626
class Int32_2(Structure):
    _fields_ = [("array", c_int32 * 2)]


# liblonlat_bng.dylib
file_path = os.path.dirname(__file__)
lib = cdll.LoadLibrary(os.path.join(file_path, 'liblonlat_bng.' + ext))
rust_bng = lib.convert
rust_bng.argtypes = [c_float, c_float]
rust_bng.restype = Int32_2

def convertbng(lon, lat):
    """ Simple wrapper around the linked Rust function """
    return tuple(r for r in rust_bng(lon, lat).array)


class FFITuple(Structure):
    _fields_ = [("a", c_uint32),
                ("b", c_uint32)]

class FFIArray(Structure):
    _fields_ = [("data", c_void_p),
                ("len", c_size_t)]

    # Allow implicit conversions from a sequence of 32-bit unsigned
    # integers.
    @classmethod
    def from_param(cls, seq):
        return seq if isinstance(seq, cls) else cls(seq)

    # Wrap sequence of values. You can specify another type besides a
    # 32-bit unsigned integer.
    def __init__(self, seq, data_type = c_float):
        array_type = data_type * len(seq)
        raw_seq = array_type(*seq)
        self.data = cast(raw_seq, c_void_p)
        self.len = len(seq)

# A conversion function that cleans up the result value to make it
# nicer to consume.
def void_array_to_tuple_list(array, _func, _args):
    return cast(array.data, POINTER(FFITuple * array.len))[0]

convert_vec = lib.convert_vec_c_threaded
convert_vec.argtypes = (FFIArray, FFIArray)
convert_vec.restype = FFIArray
convert_vec.errcheck = void_array_to_tuple_list

def convertbng_list(lons, lats):
    return [(i.a, i.b) for i in iter(convert_vec(lons, lats))]
