[![Build Status](https://travis-ci.org/urschrei/convertbng.png?branch=master)](https://travis-ci.org/urschrei/convertbng) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](license.txt) [![PyPI Version](https://img.shields.io/pypi/v/convertbng.svg)](https://pypi.python.org/pypi/convertbng)

#Description
A proof-of-concept utility library for converting longitude and latitude coordinates into British National Grid ([epsg:27700](http://spatialreference.org/ref/epsg/osgb-1936-british-national-grid/)) coordinates, and vice versa.  
Conversion is handled by a [Rust binary](https://github.com/urschrei/rust_bng), and is quite fast. Some not-very-thorough speed tests can be found [here](https://github.com/urschrei/lonlat_bng/blob/master/rust_BNG.ipynb).  

## Implementation
The main detail of interest is the FFI interface between Python and Rust, the Python side of which can be found [here](https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L49-L109), and the Rust side of which can be found [here](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L62-L72).  
The [ctypes](https://docs.python.org/2/library/ctypes.html) library expects C-compatible data structures, which we define in Rust (see above). We then define methods which allow us to [receive](https://github.com/urschrei/lonlat_bng/blob/master/src/lib.rs#L415-L420), [safely access](https://github.com/urschrei/lonlat_bng/blob/master/src/lib.rs#L125-L132), [return](https://github.com/urschrei/lonlat_bng/blob/master/src/lib.rs#L134-L149), and [free](https://github.com/urschrei/lonlat_bng/blob/master/src/lib.rs#L96-L105) data across the FFI boundary.  
Finally, we link the Rust conversion functions from the Python library [here](https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L112-L128). Note the `errcheck` assignments, which convert the FFI-compatible ctypes data structures to tuple lists. 



#Installation
`pip install convertbng`
## Note
`convertbng` is currently only available in Wheel format for OSX, though standard installation for `*nix` using pip from PyPI works, and **doesn't require a Rust installation**.

#Usage
`convertbng` accepts either a sequence (such as a list or numpy array) of longitude values and a sequence of latitude values, **or** a single longitude value and single latitude value. Note the return type:  
`"returns a list of two lists containing Easting and Northing integers (longs), respectively"`

**NOTE**: Coordinate pairs outside the BNG bounding box will return a result of  
`[[9999], [9999]]`, which cannot be mapped. Since transformed coordinates are guaranteed to be returned in the same order as the input, it is trivial to check for this value. Alternatively, ensure your data fall within the bounding box before transforming them:  

**Latitude**:  
East: 1.768960  
West: -6.379880  
**Longitude**:  
North: 55.811741  
South: 49.871159  

`convertlonlat` accepts either a sequence (such as a list or a numpy array) of BNG Eastings, and a sequence of BNG Northings, or a single Easting and a Single Northing. Note the return type:  
`"returns a list of two lists containing Longitude and Latitude floats, respectively"`

Both functions try to be liberal about what containers they accept: `list`, `tuple`, `array.array`, `numpy.ndarray`, and pretty much anything that has the `__iter__` attribute should work, including generators.

```python
from convertbng.util import convertbng, convertlonlat

# convert a single value
res = convertbng(lon, lat)

# convert lists of longitude and latitude values to BNG Eastings and Northings
lons = [lon1, lon2, lon3]
lats = [lat1, lat2, lat3]
res_list = convertbng(lons, lats)

# convert lists of BNG Eastings and Northings to longitude, latitude
eastings = [easting1, easting2, easting3]
northings = [northing1, northing2, northing3]
res_list_en = convertlonlat(eastings, northings)

# assumes numpy imported as np
lons_np = np.array(lons)
lats_np = np.array(lats)
res_list_np = convertbng(lons_np, lats_np)
```

#Building the binary for local development
- ensure you have Rust 1.x and Cargo installed
- clone https://github.com/urschrei/lonlat_bng, and ensure it's adjacent to this dir (i.e. `code/witnessme/convertbng` and `code/witnessme/rust_bng`)
- in this dir, run `make clean` then `make build`

#Tests
You can run the Python module tests by running "make test".  
Tests require both `numpy` and `nose`.

#License
[MIT](license.txt)
