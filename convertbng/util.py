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
from array import array
import numpy as np
import os

if platform == "darwin":
    ext = "dylib"
else:
    ext = "so"

__author__ = u"Stephan Hügel"
__version__ = "0.2.3"

file_path = os.path.dirname(__file__)
lib = cdll.LoadLibrary(os.path.join(file_path, 'liblonlat_bng.' + ext))


class _BNG_FFIArray(Structure):
    """ Convert sequence of floats to a C-compatible void array """
    _fields_ = [("data", c_void_p),
                ("len", c_size_t)]

    @classmethod
    def from_param(cls, seq):
        """  Allow implicit conversions from a sequence of 32-bit floats."""
        return seq if isinstance(seq, cls) else cls(seq)

    def __init__(self, seq, data_type = c_float):
        """
        Convert sequence of values into array, then ctypes Structure

        Rather than checking types (bad), we just try to blam seq
        into a ctypes object using from_buffer. If that doesn't work,
        we try successively more conservative approaches:
        numpy array -> array.array -> read-only buffer -> CPython iterable
        """
        try:
            len(seq)
        except TypeError:
             # we've got an iterator or a generator, so consume it
            seq = array('f', seq)
        array_type = data_type * len(seq)
        try:
            raw_seq = array_type.from_buffer(seq.astype(np.float32))
        except (TypeError, AttributeError):
            try:
                raw_seq = array_type.from_buffer_copy(seq.astype(np.float32))
            except (TypeError, AttributeError):
                # it's a list or a tuple
                raw_seq = array_type.from_buffer(array('f', seq))
        self.data = cast(raw_seq, c_void_p)
        self.len = len(seq)


class _BNG_RESTuple(Structure):
    """ Container for returned FFI BNG data """
    _fields_ = [("e", _BNG_FFIArray),
                ("n", _BNG_FFIArray)]


def _bng_void_array_to_tuple_list(restuple, _func, _args):
    """ Convert the lon, lat --> BNG FFI result to Python data structures """
    eastings = POINTER(c_uint32 * restuple.e.len).from_buffer_copy(restuple.e)[0]
    northings = POINTER(c_uint32 * restuple.n.len).from_buffer_copy(restuple.n)[0]
    res_list = [list(eastings), list(northings)]
    drop_bng_array(restuple.e, restuple.n)
    return res_list


class _LONLAT_FFIArray(Structure):
    """ convert sequence of ints to a C-compatible void array """
    _fields_ = [("data", c_void_p),
                ("len", c_size_t)]

    @classmethod
    def from_param(cls, seq):
        """  Allow implicit conversions from a sequence of 32-bit unsigned ints """
        return seq if isinstance(seq, cls) else cls(seq)

    def __init__(self, seq, data_type = c_uint32):
        """
        Convert sequence of values into array, then ctypes Structure

        Rather than checking types (bad), we just try to blam seq
        into a ctypes object using from_buffer. If that doesn't work,
        we try successively more conservative approaches:
        numpy array -> array.array -> read-only buffer -> CPython iterable
        """
        try:
            len(seq)
        except TypeError:
             # we've got an iterator or a generator, so consume it
            seq = array('f', seq)
        array_type = data_type * len(seq)
        try:
            raw_seq = array_type.from_buffer(seq.astype(np.uint32))
        except (TypeError, AttributeError):
            try:
                raw_seq = array_type.from_buffer_copy(seq.astype(np.uint32))
            except (TypeError, AttributeError):
                # it's a list or a tuple
                raw_seq = array_type.from_buffer(array('i', seq))
        self.data = cast(raw_seq, c_void_p)
        self.len = len(seq)


class _LONLAT_RESTuple(Structure):
    """ Container for returned FFI lon, lat data """
    _fields_ = [("lon", _LONLAT_FFIArray),
                ("lat", _LONLAT_FFIArray)]           


def _lonlat_void_array_to_tuple_list(restuple, _func, _args):
    """ Convert the BNG --> lon, lat result to Python data structures """
    lons = POINTER(c_float * restuple.lon.len).from_buffer_copy(restuple.lon)[0]
    lats = POINTER(c_float * restuple.lat.len).from_buffer_copy(restuple.lat)[0]
    res_list = [list(lons), list(lats)]
    drop_ll_array(restuple.lon, restuple.lat)
    return res_list

# Multi-threaded FFI functions
convert_bng = lib.convert_to_bng_threaded
convert_bng.argtypes = (_BNG_FFIArray, _BNG_FFIArray)
convert_bng.restype = _BNG_RESTuple
convert_bng.errcheck = _bng_void_array_to_tuple_list

convert_lonlat = lib.convert_to_lonlat_threaded
convert_lonlat.argtypes = (_LONLAT_FFIArray, _LONLAT_FFIArray)
convert_lonlat.restype = _LONLAT_RESTuple
convert_lonlat.errcheck = _lonlat_void_array_to_tuple_list

# Free FFI-allocated memory
drop_bng_array = lib.drop_int_array
drop_bng_array.argtypes = (_BNG_FFIArray, _BNG_FFIArray)
drop_bng_array.restype = None
drop_ll_array = lib.drop_float_array
drop_ll_array.argtypes = (_LONLAT_FFIArray, _LONLAT_FFIArray)
drop_ll_array.restype = None

# The type checks are not exhaustive. I know.
def convertbng(lons, lats):
    """
    Multi-threaded lon, lat --> BNG conversion
    Returns a list of two lists containing Easting and Northing integers (longs),
    respectively
    """
    if isinstance(lons, float):
        lons = [lons]
        lats = [lats]
    return convert_bng(lons, lats)

def convertlonlat(eastings, northings):
    """
    Multi-threaded BNG --> lon, lat conversion
    Returns a list of two lists containing Longitude and Latitude floats,
    respectively
    """
    if isinstance(eastings, (int, long)):
        eastings = [eastings]
        northings = [northings]
    return convert_lonlat(eastings, northings)
