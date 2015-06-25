#Description
A utility library for converting longitude and latitude coordinates into British National Grid ([epsg:27700](http://spatialreference.org/ref/epsg/osgb-1936-british-national-grid/)) coordinates.  
Conversion is handled by a Rust binary, and is quite fast. Some not-very-thorough tests can be found [here](https://github.com/urschrei/rust_bng/blob/master/rust_BNG.ipynb).

#Installation
`pip install convertbng`

#Usage
`convertbng` accepts a longitude value and a latitude value, floating-point.  
It returns a tuple of Easting and Northing integers.  

`convertbng_list` accepts a list of longitude values, and a list of latitude values.  
It returns a list of tuples containing Easting and Northing integers.


    from convertbng.util import convertbng, convertbng_list

    res = convertbng(lon, lat)
    res_list = convertbng([lons], [lats])

#Building the binary for local development
- clone https://github.com/urschrei/rust_bng
- build the dylib using cargo (see README)
- copy the binary to `convertbng/`

#License
[MIT](license.txt)
