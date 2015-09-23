[![Build Status](https://travis-ci.org/urschrei/convertbng.png?branch=master)](https://travis-ci.org/urschrei/convertbng)  
#Description
A proof-of-concept utility library for converting longitude and latitude coordinates into British National Grid ([epsg:27700](http://spatialreference.org/ref/epsg/osgb-1936-british-national-grid/)) coordinates, and vice versa.  
Conversion is handled by a [Rust binary](https://github.com/urschrei/rust_bng), and is quite fast. Some not-very-thorough tests can be found [here](https://github.com/urschrei/rust_bng/blob/master/rust_BNG.ipynb).  

## Implementation
The main detail of interest is the FFI interface between Python and Rust, the Python side of which can be found [here](https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L62-L117), and the Rust side of which can be found [here](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L369-L441).  
The [ctypes](https://docs.python.org/2/library/ctypes.html) library expects C-compatible data structures, which we define in Rust [here](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L42-L58). We then define methods on the `Array` struct, [here](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L66-L92), which allow us to receive and return data across the FFI boundary.  
Finally, we refer to the Rust conversion functions from the Python library [here](https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L125-L134). Note the `errcheck` assignments, which convert the Rust data structures to tuple lists. 



#Installation
`pip install convertbng`
## Note
`convertbng` is currently only available for OSX on PyPI, until I figure out a sensible workflow for building Linux wheels. However, you can still install it using pip: `pip install git+git://github.com/urschrei/convertbng.git`

#Usage
`convertbng` accepts a longitude value and a latitude value, floating-point.  
It returns a tuple of Easting and Northing integers.  

`convertbng_list` accepts a list of longitude values, and a list of latitude values. Numpy arrays are OK too, but note the return type:  
returns a list of tuples containing Easting and Northing integers.

`convertlonlat_list` accepts a list of BNG Eastings, and a list of BNG Northings. Numpy arrays are OK too, but note the return type:  
returns a list of tuples containing longitudes and latitudes as floating-point numbers.

```python
from convertbng.util import convertbng, convertbng_list, convertlonlat_list

# convert a single value
res = convertbng(lon, lat)

# convert lists of longitude and latitude values to BNG Eastings and Northings
lons = [lon1, lon2, lon3]
lats = [lat1, lat2, lat3]
res_list = convertbng_list(lons, lats)

# convert lists of BNG Eastings and Northings to longitude, latitude
eastings = [easting1, easting2, easting3]
northings = [northing1, northing2, northing3]
res_list_en = convertlonlat_list(eastings, northings)

# assumes numpy imported as np
lons_np = np.array(lons)
lats_np = np.array(lats)
res_list_np = convertbng_list(lons_np, lats_np)
```

#Building the binary for local development
- ensure you have Rust 1.x and Cargo installed
- clone https://github.com/urschrei/rust_bng, and ensure it's adjacent to this dir (i.e. `code/witnessme/convertbng` and `code/witnessme/rust_bng`)
- in this dir, run `make clean` then `make build`

#License
[MIT](license.txt)
