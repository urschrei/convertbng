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
from ctypes import (
    cdll,
    c_double,
    Structure,
    c_void_p,
    cast,
    c_size_t,
    POINTER,
    string_at,
)
from sys import platform, version_info
from array import array
import numpy as np
import os

__author__ = u"Stephan Hügel"
__version__ = "0.6.38"

file_path = os.path.dirname(__file__)

if platform == "darwin":
    prefix = "lib"
    ext = "dylib"
elif "linux" in platform:
    prefix = "lib"
    ext = "so"
    fpath = os.path.join(file_path, ".libs")

elif "win32" in platform:
    prefix = ""
    ext = "dll"

prefix = {"win32": ""}.get(platform, "lib")
extension = {"darwin": ".dylib", "win32": ".dll"}.get(platform, ".so")

# Python 3 check
if version_info > (3, 0):
    from subprocess import getoutput as spop

    py3 = True
else:
    from subprocess import check_output as spop

    py3 = False

try:
    lib = cdll.LoadLibrary(os.path.join(file_path, prefix + "lonlat_bng" + extension))
except OSError:
    # the Rust lib's been grafted by manylinux1
    if not py3:
        fname = spop(["ls", fpath]).split()[0]
    else:
        fname = spop(["ls %s" % fpath]).split()[0]
    lib = cdll.LoadLibrary(os.path.join(file_path, ".libs", fname))


class _FFIArray(Structure):
    """Convert sequence of floats to a C-compatible void array"""

    _fields_ = [("data", c_void_p), ("len", c_size_t)]

    @classmethod
    def from_param(cls, seq):
        """Allow implicit conversions from a sequence of 64-bit floats."""
        return seq if isinstance(seq, cls) else cls(seq)

    def __init__(self, seq, data_type=c_double):
        """
        Convert sequence of values into array, then ctypes Structure

        Rather than checking types (bad), we just try to blam seq
        into a ctypes object using from_buffer. If that doesn't work,
        we try successively more conservative approaches:
        numpy array -> array.array -> read-only buffer -> CPython iterable
        """
        if isinstance(seq, float):
            seq = array("d", [seq])
        try:
            len(seq)
        except TypeError:
            # we've got an iterator or a generator, so consume it
            seq = array("d", seq)
        array_type = data_type * len(seq)
        try:
            raw_seq = array_type.from_buffer(seq.astype(np.float64))
        except (TypeError, AttributeError):
            try:
                raw_seq = array_type.from_buffer_copy(seq.astype(np.float64))
            except (TypeError, AttributeError):
                # it's a list or a tuple
                raw_seq = array_type.from_buffer(array("d", seq))
        self.data = cast(raw_seq, c_void_p)
        self.len = len(seq)


class _Result_Tuple(Structure):
    """Container for returned FFI data"""

    _fields_ = [("e", _FFIArray), ("n", _FFIArray)]


def _void_array_to_list(restuple, _func, _args):
    """Convert the FFI result to Python data structures"""
    shape = (restuple.e.len, 1)
    array_size = np.prod(shape)
    mem_size = 8 * array_size

    array_str_e = string_at(restuple.e.data, mem_size)
    array_str_n = string_at(restuple.n.data, mem_size)

    ls_e = np.frombuffer(array_str_e, float, array_size).tolist()
    ls_n = np.frombuffer(array_str_n, float, array_size).tolist()

    return ls_e, ls_n


# Multi-threaded FFI functions
convert_bng = lib.convert_to_bng_threaded
convert_bng.argtypes = (_FFIArray, _FFIArray)
convert_bng.restype = _Result_Tuple
convert_bng.errcheck = _void_array_to_list
convert_bng.__doc__ = """
    Multi-threaded lon, lat --> BNG conversion
    Returns a list of two lists containing Easting and Northing floats,
    respectively
    Uses the Helmert transform
    """

convert_lonlat = lib.convert_to_lonlat_threaded
convert_lonlat.argtypes = (_FFIArray, _FFIArray)
convert_lonlat.restype = _Result_Tuple
convert_lonlat.errcheck = _void_array_to_list
convert_lonlat.__doc__ = """
    Multi-threaded BNG --> lon, lat conversion
    Returns a list of two lists containing Longitude and Latitude floats,
    respectively
    Uses the Helmert transform
    """

convert_to_osgb36 = lib.convert_to_osgb36_threaded
convert_to_osgb36.argtypes = (_FFIArray, _FFIArray)
convert_to_osgb36.restype = _Result_Tuple
convert_to_osgb36.errcheck = _void_array_to_list
convert_to_osgb36.__doc__ = """
    Multi-threaded lon, lat --> OSGB36 conversion, using OSTN02 data
    Returns a list of two lists containing Easting and Northing floats,
    respectively
    """

convert_osgb36_to_lonlat = lib.convert_osgb36_to_ll_threaded
convert_osgb36_to_lonlat.argtypes = (_FFIArray, _FFIArray)
convert_osgb36_to_lonlat.restype = _Result_Tuple
convert_osgb36_to_lonlat.errcheck = _void_array_to_list
convert_osgb36_to_lonlat.__doc__ = """
    Multi-threaded OSGB36 --> Lon, Lat conversion, using OSTN02 data
    Returns a list of two lists containing Easting and Northing floats,
    respectively
    """

convert_etrs89_to_lonlat = lib.convert_etrs89_to_ll_threaded
convert_etrs89_to_lonlat.argtypes = (_FFIArray, _FFIArray)
convert_etrs89_to_lonlat.restype = _Result_Tuple
convert_etrs89_to_lonlat.errcheck = _void_array_to_list
convert_etrs89_to_lonlat.__doc__ = """
    Multi-threaded ETRS89 Eastings and Northings --> OSGB36 conversion, using OSTN02 data
    Returns a list of two lists containing Easting and Northing floats,
    respectively
    """

convert_etrs89_to_osgb36 = lib.convert_etrs89_to_osgb36_threaded
convert_etrs89_to_osgb36.argtypes = (_FFIArray, _FFIArray)
convert_etrs89_to_osgb36.restype = _Result_Tuple
convert_etrs89_to_osgb36.errcheck = _void_array_to_list
convert_etrs89_to_osgb36.__doc__ = """
    Multi-threaded OSGB36 Eastings and Northings --> ETRS89 Eastings and Northings conversion,
    using OSTN02 data
    Returns a list of two lists containing Easting and Northing floats,
    respectively
    """

convert_osgb36_to_etrs89 = lib.convert_osgb36_to_etrs89_threaded
convert_osgb36_to_etrs89.argtypes = (_FFIArray, _FFIArray)
convert_osgb36_to_etrs89.restype = _Result_Tuple
convert_osgb36_to_etrs89.errcheck = _void_array_to_list
convert_osgb36_to_etrs89.__doc__ = """
    Multi-threaded ETRS89 Eastings and Northings --> Lon, Lat conversion,
    Returns a list of two lists containing Longitude and Latitude floats,
    respectively
    """

convert_epsg3857_to_wgs84 = lib.convert_epsg3857_to_wgs84_threaded
convert_epsg3857_to_wgs84.argtypes = (_FFIArray, _FFIArray)
convert_epsg3857_to_wgs84.restype = _Result_Tuple
convert_epsg3857_to_wgs84.errcheck = _void_array_to_list
convert_epsg3857_to_wgs84.__doc__ = """
    Convert Google Web Mercator (EPSG3857) coordinates to WGS84
    Latitude and Longitude
    Returns a list of two lists containing latitudes and longitudes,
    respectively
    """

convert_to_etrs89 = lib.convert_to_etrs89_threaded
convert_to_etrs89.argtypes = (_FFIArray, _FFIArray)
convert_to_etrs89.restype = _Result_Tuple
convert_to_etrs89.errcheck = _void_array_to_list
convert_to_etrs89.__doc__ = """
    Transform longitudes and latitudes to ETRS89 Eastings and Northings (without OSTN15 corrections)
    Returns a list of two lists containing Easting and Northing floats,
    respectively
    """

# Free FFI-allocated memory
drop_array = lib.drop_float_array
drop_array.argtypes = (_FFIArray, _FFIArray)
drop_array.restype = None
