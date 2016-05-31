#ifndef RLIB_H
#define RLIB_H

typedef struct _FFIArray {
  void* data;
  size_t len;
} _FFIArray;

typedef struct _Result_Tuple {
    _FFIArray e;
    _FFIArray n;
} _Result_Tuple;

_Result_Tuple convert_to_bng_threaded(_FFIArray x, _FFIArray y);
_Result_Tuple convert_to_lonlat_threaded(_FFIArray x, _FFIArray y);
_Result_Tuple convert_to_osgb36_threaded(_FFIArray x, _FFIArray y);
_Result_Tuple convert_to_etrs89_threaded(_FFIArray x, _FFIArray y);
_Result_Tuple convert_etrs89_to_osgb36_threaded(_FFIArray x, _FFIArray y);
_Result_Tuple convert_etrs89_to_ll_threaded(_FFIArray x, _FFIArray y);
_Result_Tuple convert_osgb36_to_ll_threaded(_FFIArray x, _FFIArray y);
_Result_Tuple convert_osgb36_to_etrs89_threaded(_FFIArray x, _FFIArray y);
_Result_Tuple convert_epsg3857_to_wgs84_threaded(_FFIArray x, _FFIArray y);
void drop_float_array(_FFIArray x, _FFIArray y);

#endif
