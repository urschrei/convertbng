============================================================================
Fast longitude, latitude to British National Grid conversion, and vice versa
============================================================================
| Fast longitude, latitude to `BNG <https://en.wikipedia.org/wiki/Ordnance_Survey_National_Grid>`_ conversion, and vice versa, using a multithreaded `Rust <https://www.rust-lang.org>`_ `binary <https://github.com/urschrei/lonlat_bng>`_ and FFI.

| This module provides two methods: 

| ``util.convertbng(lons, lats)`` – pass sequences (such as lists or numpy arrays) of Longitudes andLatitudes, or single values of each. Returns a list of two lists containing Easting and Northing integers (longs), respectively.
| ``util.convertlonlat(eastings, northings)`` – pass sequences (such as lists or numpy arrays) of Eastings, Northings, or single values of each. Returns a list of two lists containing Longitude and Latitude floats, respectively
| 
| NOTE: Coordinate pairs outside the BNG bounding box will return a result of  ``[[9999], [9999]]``, which cannot be mapped. Since transformed coordinates are guaranteed to be returned in the same order as the input, it is trivial to check for this value. Alternatively, ensure your data fall within the bounding box before transforming them:
|
| **Latitude**:  
| East: 1.768960 (Max)
| West: -6.379880 (Min)

| **Longitude**:  
| North: 55.811741 (Max)
| South: 49.871159 (Min)

Installation
============
|  Installation as a binary wheel using pip, for OS X: 
|  ``pip install convertbng`` 

|  Binary wheels aren't yet available for Linux or Windows, but installation directly from Github works: 
|  ``pip install git+git://github.com/urschrei/convertbng.git`` 

Usage
=====

.. code-block:: python

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

Testing
=======
Run ``nosetests`` (requires `Nose <http://nose.readthedocs.org/en/latest/>`_)
