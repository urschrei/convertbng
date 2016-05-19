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
void drop_float_array(_FFIArray x, _FFIArray y);

#endif