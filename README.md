[![Build Status](https://travis-ci.org/urschrei/convertbng.png?branch=master)](https://travis-ci.org/urschrei/convertbng)  
#Description
A proof-of-concept utility library for converting longitude and latitude coordinates into British National Grid ([epsg:27700](http://spatialreference.org/ref/epsg/osgb-1936-british-national-grid/)) coordinates, and vice versa.  
Conversion is handled by a [Rust binary](https://github.com/urschrei/rust_bng), and is quite fast. Some not-very-thorough tests can be found [here](https://github.com/urschrei/rust_bng/blob/master/rust_BNG.ipynb).  

## Implementation
The main detail of interest is the FFI interface between Python and Rust, the Python side of which can be found [here](https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L48-L108), and the Rust side of which can be found [here](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L63-L115).  
The [ctypes](https://docs.python.org/2/library/ctypes.html) library expects C-compatible data structures, which we define in Rust (see above). We then define methods which allow us to [receive](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L368-L375), [safely access](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L90-L97), [return](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L99-L114), and [free](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L69-L87) data across the FFI boundary.  
Finally, we refer to the Rust conversion functions from the Python library [here](https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L111-L128). Note the `errcheck` assignments, which convert the Rust data structures to tuple lists. 



#Installation
`pip install convertbng`
## Note
`convertbng` is currently only available in Wheel format for OSX, though standard installation for `*nix` using pip from PyPI works, and **doesn't require a Rust installation**.

#Usage
`convertbng` accepts either a single longitude value and single latitude value, **or** a list of longitude values and a list of latitude values. Numpy arrays are OK too, but note the return type:  
`"returns a list of tuples containing Easting and Northing integers (longs)."`

`convertlonlat` accepts either a single Easting and a Single Northing, or a list of BNG Eastings, and a list of BNG Northings. Numpy arrays are OK too, but note the return type:  
`"returns a list of tuples containing longitudes and latitudes as floating-point numbers."`

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
- clone https://github.com/urschrei/rust_bng, and ensure it's adjacent to this dir (i.e. `code/witnessme/convertbng` and `code/witnessme/rust_bng`)
- in this dir, run `make clean` then `make build`

#Tests
You can run the Python module tests by running "make test".  
Tests require both `numpy` and `nose`.

#License
[MIT](license.txt)
