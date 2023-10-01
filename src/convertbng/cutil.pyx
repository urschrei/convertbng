#cython: boundscheck=False
# -*- coding: utf-8 -*-
"""
cutil.pyx

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
__author__ = u"Stephan Hügel"

import numpy as np
from convertbng_p cimport (
    Array,
    ResultTuple,
    convert_to_bng_threaded,
    convert_to_lonlat_threaded,
    convert_to_osgb36_threaded,
    convert_to_etrs89_threaded,
    convert_etrs89_to_osgb36_threaded,
    convert_etrs89_to_ll_threaded,
    convert_osgb36_to_ll_threaded,
    convert_osgb36_to_etrs89_threaded,
    convert_epsg3857_to_wgs84_threaded,
    drop_float_array
    )

# should catch a ValueError here, in case something non-double is passed
cdef ffi_wrapper(ResultTuple (*func)(Array, Array)):
    """ Accepts a function pointer and two arguments
            longitudes
            latitudes
    These must be memory-contiguous Python arrays
    The function pointer must map to an external FFI Rust function
    """
    def wrapped(inlon, inlat):
        # Assumes that the data is double, not float. This is easily changed
        # The [::1] promises it's contiguous in memory
        cdef double[::1] wlon = np.array(inlon, dtype=np.float64)
        cdef double [::1] wlat = np.array(inlat, dtype=np.float64)
        cdef Array x_ffi, y_ffi
        # get a pointer to the data, and cast it to void*
        x_ffi.data = <void*>&wlon[0]
        # This may be ... * sizeof(double) - it depends on the C api
        x_ffi.len = wlon.shape[0]
        # repeat for lats
        y_ffi.data = <void*>&wlat[0]
        y_ffi.len = wlat.shape[0]
        # call across the FFI boundary
        cdef ResultTuple result = func(x_ffi, y_ffi)
        # get data pointers for the two result arrays
        cdef double* eastings_ptr = <double*>(result.e.data)
        cdef double* northings_ptr = <double*>(result.n.data)
        # now view the output arrays using memoryviews
        # their length must be specified
        cdef double[::1] e = <double[:result.e.len:1]>eastings_ptr
        cdef double[::1] n = <double[:result.n.len:1]>northings_ptr
        # create numpy copies of the two arrays
        e_numpy = np.copy(e)
        n_numpy = np.copy(n)
        return e_numpy, n_numpy
    return wrapped

convert_bng = ffi_wrapper(&convert_to_bng_threaded)
convert_lonlat = ffi_wrapper(&convert_to_lonlat_threaded)
convert_to_osgb36 = ffi_wrapper(&convert_to_osgb36_threaded)
convert_to_etrs89 = ffi_wrapper(&convert_to_etrs89_threaded)
convert_etrs89_to_osgb36 = ffi_wrapper(&convert_etrs89_to_osgb36_threaded)
convert_etrs89_to_ll = ffi_wrapper(&convert_etrs89_to_ll_threaded)
convert_osgb36_to_ll = ffi_wrapper(&convert_osgb36_to_ll_threaded)
convert_osgb36_to_etrs89 = ffi_wrapper(&convert_osgb36_to_etrs89_threaded)
convert_epsg3857_to_wgs84 = ffi_wrapper(&convert_epsg3857_to_wgs84_threaded)
