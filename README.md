[![Build Status](https://travis-ci.org/urschrei/convertbng.png?branch=master)](https://travis-ci.org/urschrei/convertbng)  
#Description
A utility library for converting longitude and latitude coordinates into British National Grid ([epsg:27700](http://spatialreference.org/ref/epsg/osgb-1936-british-national-grid/)) coordinates.  
Conversion is handled by a Rust binary, and is quite fast. Some not-very-thorough tests can be found [here](https://github.com/urschrei/rust_bng/blob/master/rust_BNG.ipynb).

#Installation
`pip install convertbng`
## Note
`convertbng` is currently only available for OSX on PyPI, until I figure out a sensible workflow for building Linux wheels. However, you can still install it using pip: `pip install git+git://github.com/urschrei/convertbng.git`

#Usage
`convertbng` accepts a longitude value and a latitude value, floating-point.  
It returns a tuple of Easting and Northing integers.  

`convertbng_list` accepts a list of longitude values, and a list of latitude values. Numpy arrays are OK too, but note the return type:  
returns a list of tuples containing Easting and Northing integers.


    from convertbng.util import convertbng, convertbng_list


    lons = [lon1, lon2, lon3]
    lats = [lat1, lat2, lat3]
    # assumes you've imported numpy as np
    lons_np = np.array(lons)
    lats_np = np.array(lats)

    res = convertbng(lon, lat)
    res_list = convertbng_list(lons, lats)
    res_np = convertbng_list(lons_np, lats_np)

#Building the binary for local development
- ensure you have Rust 1.x and Cargo installed
- clone https://github.com/urschrei/rust_bng, and ensure it's adjacent to this dir (i.e. `code/witnessme/convertbng` and `code/witnessme/rust_bng`)
- in this dir, run `make clean` then `make build`

#License
[MIT](license.txt)
