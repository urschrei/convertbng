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
from ctypes import cdll, c_uint32, c_float, Structure, c_void_p, cast, c_size_t, POINTER
from sys import platform
import os

if platform == "darwin":
    ext = "dylib"
else:
    ext = "so"

__author__ = u"Stephan Hügel"
__version__ = "0.1.22"

file_path = os.path.dirname(__file__)
lib = cdll.LoadLibrary(os.path.join(file_path, 'liblonlat_bng.' + ext))


class _BNG_FFITuple(Structure):
    _fields_ = [("a", c_uint32),
                ("b", c_uint32)]


class _BNG_FFIArray(Structure):
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
def _bng_void_array_to_tuple_list(array, _func, _args):
    res = cast(array.data, POINTER(_BNG_FFITuple * array.len))[0]
    res_list = [(i.a, i.b) for i in iter(res)]
    drop_bng_array(array)
    return res_list


class _LONLAT_FFITuple(Structure):
    _fields_ = [("a", c_float),
                ("b", c_float)]


class _LONLAT_FFIArray(Structure):
    _fields_ = [("data", c_void_p),
                ("len", c_size_t)]
    # Allow implicit conversions from a sequence of 32-bit unsigned
    # integers.
    @classmethod
    def from_param(cls, seq):
        return seq if isinstance(seq, cls) else cls(seq)

    # Wrap sequence of values. You can specify another type besides a
    # 32-bit unsigned integer.
    def __init__(self, seq, data_type = c_uint32):
        array_type = data_type * len(seq)
        raw_seq = array_type(*seq)
        self.data = cast(raw_seq, c_void_p)
        self.len = len(seq)


# A conversion function that cleans up the result value to make it
# nicer to consume.
def _lonlat_void_array_to_tuple_list(array, _func, _args):
    res = cast(array.data, POINTER(_LONLAT_FFITuple * array.len))[0]
    res_list = [(i.a, i.b) for i in iter(res)]
    drop_ll_array(array)
    return res_list


# Multi-threaded
convert_bng = lib.convert_to_bng_threaded
convert_bng.argtypes = (_BNG_FFIArray, _BNG_FFIArray)
convert_bng.restype = _BNG_FFIArray
convert_bng.errcheck = _bng_void_array_to_tuple_list

convert_lonlat = lib.convert_to_lonlat_threaded
convert_lonlat.argtypes = (_LONLAT_FFIArray, _LONLAT_FFIArray)
convert_lonlat.restype = _LONLAT_FFIArray
convert_lonlat.errcheck = _lonlat_void_array_to_tuple_list

# cleanup
drop_bng_array = lib.drop_int_array
drop_bng_array.argtypes = (_BNG_FFIArray,)
drop_bng_array.restype = None
drop_ll_array = lib.drop_float_array
drop_ll_array.argtypes = (_LONLAT_FFIArray,)
drop_ll_array.restype = None


# The module exports these functions
def convertbng(lon, lat):
    """ Single-threaded lon, lat --> BNG conversion """
    return convert_bng([lon], [lat])[0]

def convertbng_list(lons, lats):
    """ Multi-threaded lon, lat --> BNG conversion """
    return convert_bng(lons, lats)

def convertlonlat_list(eastings, northings):
    """ Multi-threaded BNG --> lon, lat conversion """
    return convert_lonlat(eastings, northings)
