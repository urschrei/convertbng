|Build Status| |Coverage Status| |MIT licensed| |PyPI Version|

Description
===========

A utility library for converting decimal
`WGS84 <http://spatialreference.org/ref/epsg/wgs-84/>`__ longitude and
latitude coordinates into ETRS89
(`EPSG:25830 <http://spatialreference.org/ref/epsg/etrs89-utm-zone-30n/>`__)
and/or British National Grid (More correctly: OSGB36, or
`EPSG:27700 <http://spatialreference.org/ref/epsg/osgb-1936-british-national-grid/>`__)
Eastings and Northings, and vice versa.

Conversion is handled by a `Rust
binary <https://github.com/urschrei/rust_bng>`__ using FFI, and is quite
fast. Some not-very-thorough speed tests can be found
`here <https://github.com/urschrei/lonlat_bng/blob/master/rust_BNG.ipynb>`__.
Generally speaking, conversion of one million coordinate pairs takes
just over half a second.

Installation
============

``pip install convertbng``

Note
----

``convertbng`` is currently only available in Wheel format for OSX,
though standard installation for ``*nix`` using pip from PyPI works, and
**doesn't require a Rust installation**.

Usage
=====

| The functions accept either a sequence (such as a list or numpy array)
  of longitude or easting values and a sequence of latitude or northing
  values, **or** a single longitude/easting value and single
  latitude/northing value. Note the return type:
| ``"returns a list of two lists containing floats, respectively"``

| **NOTE**: Coordinate pairs outside the BNG bounding box, or without
  OSTN02 coverage will return a result of
| ``[[nan], [nan]]``, which cannot be mapped. Since transformed
  coordinates are guaranteed to be returned in the same order as the
  input, it is trivial to check for this value. Alternatively, ensure
  your data fall within the bounding box before transforming them:

| **Latitude**:
| East: 1.7800
| West: -7.5600
| **Longitude**:
| North: 60.8400
| South: 49.9600

All functions try to be liberal about what containers they accept:
``list``, ``tuple``, ``array.array``, ``numpy.ndarray``, and pretty much
anything that has the ``__iter__`` attribute should work, including
generators.

.. code:: python

    from convertbng.util import convert_bng, convert_lonlat

    # convert a single value
    res = convert_bng(lon, lat)

    # convert lists of longitude and latitude values to OSGB36 Eastings and Northings, using OSTN02 corrections
    lons = [lon1, lon2, lon3]
    lats = [lat1, lat2, lat3]
    res_list = convert_bng(lons, lats)

    # convert lists of BNG Eastings and Northings to longitude, latitude
    eastings = [easting1, easting2, easting3]
    northings = [northing1, northing2, northing3]
    res_list_en = convert_lonlat(eastings, northings)

    # assumes numpy imported as np
    lons_np = np.array(lons)
    lats_np = np.array(lats)
    res_list_np = convert_bng(lons_np, lats_np)

I Want To…
----------

-  transform longitudes and latitudes to OSGB36 Eastings and Northings
   **very accurately**:

   -  use ``convert_bng()``

-  transform OSGB36 Eastings and Northings to latitude and longitude,
   **very accurately**:

   -  use ``convert_lonlat()``

-  transform longitudes and latitudes to ETRS89 Eastings and Northings,
   **very quickly** (without OSTN02 corrections):

   -  use ``convert_etrs89()``

-  transform ETRS89 Eastings and Northings to ETRS89 latitude and
   longitude, **very quickly** (the transformation does not use OSTN02):

   -  use ``convert_etrs89_to_lonlat()``

-  convert ETRS89 Eastings and Northings to their most accurate
   real-world representation, using the OSTN02 corrections:

   -  use ``convert_etrs89_to_osgb36()``

Provided for completeness:

-  transform accurate OSGB36 Eastings and Northings to *less-accurate*
   ETRS89 Eastings and Northings:

   -  use ``convert_osgb36_to_etrs89()``

-  transform ETRS89 Eastings and Northings to ETRS89 longitude and
   latitude:

   -  use ``convert_etrs89_to_lonlat()``

Relationship between ETRS89 and WGS84
=====================================

From *`Transformations and OSGM02™, User
guide <https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/formats-for-developers.html>`__*,
p7. Emphasis mine. >[…] In Europe, ETRS89 is a precise version of the
better known WGS84 reference system optimised for use in Europe;
**however, for most purposes it can be considered equivalent to WGS84**.
Specifically, the motion of the European continental plate is not
apparent in ETRS89, which allows a fixed relationship to be established
between this system and Ordnance Survey mapping coordinate systems.
Additional precise versions of WGS84 are currently in use, notably ITRS;
these are not equivalent to ETRS89. The difference between ITRS and
ETRS89 is in the order of 0.25 m (in 1999), and growing by 0.025 m per
year in UK and Ireland. This effect is only relevant in international
scientific applications. **For all navigation, mapping, GIS, and
engineering applications within the tectonically stable parts of Europe
(including UK and Ireland), the term ETRS89 should be taken as
synonymous with WGS84**.

In essence, this means that anywhere you see ETRS89 in this README, you
can substitute WGS84.

What CRS Are My Data In
-----------------------

-  if you have latitude and longitude coordinates:

   -  They're probably
      `WGS84 <http://spatialreference.org/ref/epsg/wgs-84/>`__.
      Everything's fine!

-  if you got your coordinates from a smartphone or a consumer GPS:

   -  They're probably
      `WGS84 <http://spatialreference.org/ref/epsg/wgs-84/>`__.
      Everything's fine!

-  if you have x and y coordinates, or you got your coordinates from
   Google Maps or Bing Maps and they look something like
   ``(-626172.1357121646, 6887893.4928337997)``, or the phrase
   "Spherical Mercator" is mentioned anywhere:

   -  they're probably in `Web
      Mercator <http://spatialreference.org/ref/sr-org/6864/>`__. You
      **must** convert them to WGS84 first. Use
      ``convert_epsg3857_to_wgs84([x_coordinates], [y_coordinates])`` to
      do so.

Accuracy
========

``convert_bng`` and ``convert_lonlat`` use the standard seven-step
`Helmert
transform <https://en.wikipedia.org/wiki/Helmert_transformation>`__ to
convert coordinates. This is fast, but not particularly accurate – it
can introduce positional error up to approximately 5 metres. For most
applications, this is not of particular concern – the input data
(especially those originating with smartphone GPS) probably exceed this
level of error in any case. In order to adjust for this, ``convert_bng``
then retrieves the OSTN02 adjustments for the kilometer-grid the point
falls in, and performs a linear interpolation to give final, accurate
coordinates. This process happens in reverse for ``convert_lonlat``.

OSTN02
------

`OSTN02 <https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/surveying.html>`__
data are used for highly accurate conversions from ETRS89 latitude and
longitude, or ETRS89 Eastings and Northings to OSGB36 Eastings and
Northings, and vice versa. These data will usually have been recorded
using the `National GPS
Network <https://www.ordnancesurvey.co.uk/business-and-government/products/os-net/index.html>`__:

Accuracy of *Your* Data
~~~~~~~~~~~~~~~~~~~~~~~

Conversion of your coordinates using OSTN02 transformations will be
accurate, but if you're using consumer equipment, or got your data off
the web, be aware that you're converting coordinates which probably
weren't accurately recorded in the first place. That's because `accurate
surveying is
difficult <https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/surveying.html>`__.
If you work in surveying or geodesy, you already know all this – sorry!

Accuracy of the OSTN02 transformation used in this library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ETRS89 longitude and latitude / Eastings and Northings to OSGB36
   conversion agrees with the provided Ordnance Survey test data in **31
   of the 42** test coordinates (excluding two coordinates designed to
   return no data; these correctly fail).
-  The 11 discrepancies are of **1mm** in each case.
-  OSGB36 to ETRS89 longitude and latitude conversion is accurate to
   within 8 decimal places, or 1.1mm.

A Note on Ellipsoids
~~~~~~~~~~~~~~~~~~~~

WGS84 and ETRS89 coordinates use the GRS80 ellipsoid, whereas OSGB36
uses the Airy 1830 ellipsoid, which provides a regional best fit for
Britain. Positions for coordinates in Great Britain can differ by over
100m as a result. It is thus inadvisable to attempt calculations using
mixed ETRS89 and OSGB36 coordinates.

|OSTN02|

Implementation
--------------

| The main detail of interest is the FFI interface between Python and
  Rust, the Python side of which can be found
  `here <https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L50-L99>`__,
  and the Rust side of which can be found
  `here <https://github.com/urschrei/rust_bng/blob/master/src/lib.rs#L158-L180>`__.
| The `ctypes <https://docs.python.org/2/library/ctypes.html>`__ library
  expects C-compatible data structures, which we define in Rust (see
  above). We then define methods which allow us to receive, safely
  access, return, and free data across the FFI boundary.
| Finally, we link the Rust conversion functions from the Python library
  `here <https://github.com/urschrei/convertbng/blob/master/convertbng/util.py#L102-L126>`__.
  Note the ``errcheck`` assignments, which convert the FFI-compatible
  ctypes data structures to tuple lists.

Building the binary for local development
=========================================

-  ensure you have Rust 1.x and Cargo installed
-  clone https://github.com/urschrei/lonlat\_bng, and ensure it's
   adjacent to this dir (i.e. ``code/witnessme/convertbng`` and
   ``code/witnessme/rust_bng``)
-  in this dir, run ``make clean`` then ``make build``

Tests
=====

| You can run the Python module tests by running "make test".
| Tests require both ``numpy`` and ``nose``.

License
=======

`MIT <license.txt>`__

.. |Build Status| image:: https://travis-ci.org/urschrei/convertbng.png?branch=master
   :target: https://travis-ci.org/urschrei/convertbng
.. |Coverage Status| image:: https://coveralls.io/repos/github/urschrei/convertbng/badge.svg?branch=master
   :target: https://coveralls.io/github/urschrei/convertbng?branch=master
.. |MIT licensed| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: license.txt
.. |PyPI Version| image:: https://img.shields.io/pypi/v/convertbng.svg
   :target: https://pypi.python.org/pypi/convertbng
.. |OSTN02| image:: ostn002_s.gif
   :target: %22OSTN02%22
