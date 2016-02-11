============================================================================
Fast longitude, latitude to British National Grid conversion, and vice versa
============================================================================
| Fast longitude, latitude to `BNG <https://en.wikipedia.org/wiki/Ordnance_Survey_National_Grid>`_ conversion, and vice versa, using a multithreaded `Rust <https://www.rust-lang.org>`_ `binary <https://github.com/urschrei/lonlat_bng>`_ and FFI.

| This module provides two fast methods: 

| ``util.convertbng(lons, lats)`` – pass sequences (such as lists or numpy arrays) of Longitudes and Latitudes, or single values of each. Returns a list of two lists containing Easting and Northing floats, respectively.
| ``util.convertlonlat(eastings, northings)`` – pass sequences (such as lists or numpy arrays) of Eastings, Northings, or single values of each. Returns a list of two lists containing Longitude and Latitude floats, respectively

| And four accurate `OSTN02 <https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/surveying.html>`_-enabled methods, suitable for surveying and other geodetic work:

.. note:: The OSTN02-enabled methods are envisaged to be used with accurate measurements collected using the `National GPS Network <https://www.ordnancesurvey.co.uk/business-and-government/products/os-net/index.html>`_.

| ``convert_osgb36(lons, lats)`` – convert ETRS89 Longitudes and Latitudes to OSGB36
| ``convert_osgb36_to_lonlat(eastings, northings)`` – convert OSGB36 Eastings and Northings to ETRS89 longitudes and latitudes 
| ``convert_etrs89_to_osgb36(eastings, northings)`` – convert ETRS89 Eastings and Northings to OSGB36 Eastings and Northings
| ``convert_osgb36_to_etrs89(eastings, northings)`` – convert OSGB36 eastings and Northings to ETRS89 Eastings and Northings.

| All four methods accept and return floating-point numbers. 


.. warning:: Coordinate pairs outside the BNG bounding box will return a result of  ``[[9999], [9999]]``, which cannot be mapped. Since transformed coordinates are guaranteed to be returned in the same order as the input, it is trivial to check for this value. Alternatively, ensure your data fall within the bounding box before transforming them:

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
