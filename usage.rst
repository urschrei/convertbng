=========================================
Fast lon, lat to BNG conversion, and back
=========================================
This library uses a Rust 1.x binary to perform fast longitude, latitude to `BNG <https://en.wikipedia.org/wiki/Ordnance_Survey_National_Grid>`_ conversion, and vice versa. 

|This module exposes three methods: 
|``util.convertbng()`` – pass a lon, lat. Returns a tuple of Eastings, Northings 
|``util.convertbng_list()`` – pass lists (or Numpy arrays) of lons, lats. 
|``util.convertlonlat_list()`` – pass lists (or Numpy arrays) of Eastings, Northings. 
|Both methods return Easting, Northing tuples (in a list in the case of the latter). 

Installation
============
|Installation as a binary wheel using pip, for OS X: 
|``pip install convertbng`` 
|Binary wheels aren't yet available for Linux or Windows, but installation directly from Github works: 
``pip install git+git://github.com/urschrei/convertbng.git`` 

Usage
=====

.. code-block:: python

    from convertbng.util import convertbng, convertbng_list, convertlonlat_list

    res = convertbng(lon, lat)

    lons = [lon1, lon2, lon3]
    lats = [lat1, lat2, lat3]
    eastings = [easting1, easting2, easting3]
    northings = [northing1, northing2, northing3]
    # assumes numpy imported as np
    lons_np = np.array(lons)
    lats_np = np.array(lats)
    
    res_list = convertbng_list(lons, lats)
    res_list_np = convertbng_list(lons_np, lats_np) 
    res_list_en = convertlonlat_list(eastings, northings)
