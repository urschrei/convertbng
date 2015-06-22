# -*- coding: utf-8 -*-

from ctypes import cdll, c_float, Structure, ARRAY, c_int32
from sys import platform
import os

if platform == "darwin":
    ext = "dylib"
else:
    ext = "so"

__author__ = u"Stephan Hügel"
__version__ = "0.1.7"

# hacky: http://stackoverflow.com/a/30789980/416626
class Int32_2(Structure):
    _fields_ = [("array", ARRAY(c_int32, 2))]

# liblonlat_bng.dylib
file_path = os.path.dirname(__file__)
lib = cdll.LoadLibrary(os.path.join(file_path, 'liblonlat_bng.' + ext))
rust_bng = lib.convert
rust_bng.restype = Int32_2

def convertbng(lon, lat):
    """ Simple wrapper around the linked Rust function """
    c_lon, c_lat = c_float(lon), c_float(lat)
    return tuple(r for r in rust_bng(c_lon, c_lat).array)
