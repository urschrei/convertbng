cdef extern from "header.h":
    struct Array:
        void* data
        size_t len

    struct ResultTuple:
        Array e
        Array n

    cdef ResultTuple convert_to_bng_threaded(Array x, Array y)
    cdef ResultTuple convert_to_lonlat_threaded(Array x, Array y);
    cdef ResultTuple convert_to_osgb36_threaded(Array x, Array y);
    cdef ResultTuple convert_to_etrs89_threaded(Array x, Array y);
    cdef ResultTuple convert_etrs89_to_osgb36_threaded(Array x, Array y);
    cdef ResultTuple convert_etrs89_to_ll_threaded(Array x, Array y);
    cdef ResultTuple convert_osgb36_to_ll_threaded(Array x, Array y);
    cdef ResultTuple convert_osgb36_to_etrs89_threaded(Array x, Array y);
    cdef ResultTuple convert_epsg3857_to_wgs84_threaded(Array x, Array y);
    cdef void drop_float_array(Array x, Array y)
