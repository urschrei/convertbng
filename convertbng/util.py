# -*- coding: utf-8 -*-

from ctypes import cdll, c_float, Structure, ARRAY, c_int32
from sys import platform

if platform == "darwin":
    ext = "dylib"
else:
    ext = "so"

__author__ = u"Stephan Hügel"
__version__ = "0.1"

# hacky: http://stackoverflow.com/a/30789980/416626
class Int32_2(Structure):
    _fields_ = [("array", ARRAY(c_int32, 2))]

# pretty sure this is relative to the top-level module
lib = cdll.LoadLibrary('src/liblonlat_bng.' + ext)
rust_bng = lib.convert
rust_bng.restype = Int32_2

def convert(lon, lat):
    """ Simple wrapper around the linked Rust function """
    c_lon, c_lat = c_float(lon), c_float(lat)
    return tuple(r for r in rust_bng(c_lon, c_lat).array)
