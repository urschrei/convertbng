[![Build Status](https://travis-ci.org/urschrei/convertbng.png?branch=master)](https://travis-ci.org/urschrei/convertbng) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](license.txt) [![PyPI Version](https://img.shields.io/pypi/v/convertbng.svg)](https://pypi.python.org/pypi/convertbng)

#Description
A proof-of-concept utility library for converting longitude and latitude coordinates into British National Grid ([epsg:27700](http://spatialreference.org/ref/epsg/osgb-1936-british-national-grid/)) coordinates, and vice versa.  
Conversion is handled by a [Rust binary](https://github.com/urschrei/rust_bng), and is quite fast. Some not-very-thorough speed tests can be found [here](https://github.com/urschrei/lonlat_bng/blob/master/rust_BNG.ipynb).

#Accuracy
`convertbng` and `convertlonlat` use the standard seven-step [Helmert transform](https://en.wikipedia.org/wiki/Helmert_transformation) to convert coordinates. This is fast, but not particularly accurate – it can introduce positional error up to approximately 7 metres. For most applications, this is not of particular concern – the input data (especially those originating with smartphone GPS ) probably exceed this level of error in any case.

##OSTN02
If greater accuracy is required, you may use the OSTN02-enabled functions, which use [OSTN02](https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/surveying.html) data for highly accurate conversions from ETRS89 latitude and longitude or ETRS89 Eastings and Northings to OSGB36 Eastings and Northings, and vice versa. These data will usually have been recorded using the [National GPS Network](https://www.ordnancesurvey.co.uk/business-and-government/products/os-net/index.html):

- Use **`convert_osgb36(lons, lats)`** to convert ETRS89 Longitudes and Latitudes to OSGB36
- Use **`convert_osgb36_to_lonlat(eastings, northings)`** to convert OSGB36 Eastings and Northings to ETRS89 longitudes and latitudes
- Use **`convert_etrs89_to_osgb36(eastings, northings)`** to convert ETRS89 Eastings and Northings to OSGB36 Eastings and Northings
- Use **`convert_osgb36_to_etrs89(eastings, northings)`** to convert OSGB36 eastings and Northings to ETRS89 Eastings and Northings.

###Accuracy of the OSTN02 transformation used in this library

- ETRS89 longitude and latitude / Eastings and Northings to OSGB36 conversion agrees with the provided Ordnance Survey test data in 31 of the 42 test coordinates (excluding two coordinates designed to return no data). The 11 discrepancies are of 1mm in each case.
- OSGB36 to ETRS89 longitude and latitude conversion is accurate to within 8 decimal places, or 1.1mm.

[![OSTN02](ostn002_s.gif)]( "OSTN02")

##Implementation
The main detail of interest is the FFI interface between Python and Rust, the Python side of which can be found [here](https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L50-L99), and the Rust side of which can be found [here](https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L158-L180).  
The [ctypes](https://docs.python.org/2/library/ctypes.html) library expects C-compatible data structures, which we define in Rust (see above). We then define methods which allow us to receive, safely access, return, and free data across the FFI boundary.  
Finally, we link the Rust conversion functions from the Python library [here](https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L102-L126). Note the `errcheck` assignments, which convert the FFI-compatible ctypes data structures to tuple lists. 



#Installation
`pip install convertbng`
## Note
`convertbng` is currently only available in Wheel format for OSX, though standard installation for `*nix` using pip from PyPI works, and **doesn't require a Rust installation**.

#Usage
The functions accept either a sequence (such as a list or numpy array) of longitude or easting values and a sequence of latitude or northing values, **or** a single longitude/easting value and single latitude/northing value. Note the return type:  
`"returns a list of two lists containing floats, respectively"`

**NOTE**: Coordinate pairs outside the BNG bounding box will return a result of  
`[[9999], [9999]]`, which cannot be mapped. Since transformed coordinates are guaranteed to be returned in the same order as the input, it is trivial to check for this value. Alternatively, ensure your data fall within the bounding box before transforming them:  

**Latitude**:  
East: 1.768960  
West: -6.379880  
**Longitude**:  
North: 55.811741  
South: 49.871159  

All functions try to be liberal about what containers they accept: `list`, `tuple`, `array.array`, `numpy.ndarray`, and pretty much anything that has the `__iter__` attribute should work, including generators.

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
