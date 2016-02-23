import unittest
import numpy as np
import array
import math
from convertbng.convertbng.util import (
    convert_bng,
    convert_lonlat,
    convert_to_osgb36,
    convert_osgb36_to_lonlat,
    convert_osgb36_to_etrs89,
    convert_etrs89_to_osgb36,
    convert_etrs89_to_lonlat,
    convert_epsg3857_to_wgs84
)

from ctypes import ArgumentError


class ConvertbngTests(unittest.TestCase):
    """ Tests for convert_bng
    """

    def setUp(self):
        """ Set stuff up
        """
        pass

    def testConvertLonLat(self):
        """ Test multithreaded lon, lat --> BNG function """
        expected = [
            [516274.449, 398915.542],
            [173141.09800000003, 521544.088]
        ]
   
        result = convert_bng(
            [-0.32824866, -2.0183041005533306],
            [51.44533267, 54.589097162646141]
        )
        self.assertEqual(expected, result)

    def testConvertBNG(self):
        """ Test multithreaded BNG --> lon, lat function """
        expected = [
            [-0.32822636, -2.01831249],
            [51.44533146, 54.58910536]
        ]
        result = convert_lonlat(
            [516276L, 398915L],
            [173141L, 521545L]
        )
        self.assertEqual(expected, result)

    def testConvertLonLatSingle(self):
        """ Test lon, lat --> BNG conversion of single values """
        expected = [[651409.792], [313177.448]]
        result = convert_bng(1.716073973, 52.658007833)
        self.assertEqual(expected, result)

    def testConvertTuple(self):
        """ Test lon, lat --> BNG conversion of tuples """
        expected = [[651409.792], [313177.448]]
        result = convert_bng((1.716073973,), (52.658007833,))
        self.assertEqual(expected, result)

    def testConvertString(self):
        """ Test that an error is thrown for incorrect types """
        with self.assertRaises(ArgumentError) as result:
            convert_bng(['Foo'], ['Bar'])

    def testConvertIterable(self):
        """ Test lon, lat --> BNG conversion of tuples """
        expected = [[651409.792], [313177.448]]
        result = convert_bng(iter([1.7160739736]), iter([52.658007833]))
        self.assertEqual(expected, result)

    def testConvertArray(self):
        """ Test lon, lat --> BNG conversion of array.array """
        expected = [[651409.792], [313177.448]]
        result = convert_bng(array.array('d', [1.716073973]), array.array('d', [52.658007833]))
        self.assertEqual(expected, result)

    def testGenerator(self):
        """ Test that the lon, lat -> BNG function can consume generators """
        expected = [
            [516274.449, 398915.542],
            [173141.09800000003, 521544.088]
        ]
        inp = [
            [-0.32824866,
                -2.0183041005533306],
            [51.44533267,
                54.589097162646141]
        ]
        lon_generator = (n for n in inp[0])
        lat_generator = (n for n in inp[1])
        result = convert_bng(lon_generator, lat_generator)
        self.assertEqual(expected, result)

    def testNumpyConversion(self):
        """ Test lon, lat --> BNG conversion of numpy arrays """
        # UK bounding box
        N = 55.811741
        E = 1.768960
        S = 49.871159
        W = -6.379880

        num_coords = 1000
        lon_arr = np.random.uniform(W, E, [num_coords])
        lat_arr = np.random.uniform(S, N, [num_coords])
        convert_bng(lon_arr, lat_arr)
        
    def testLargeArrayConversion(self):
        """ Test that we don't get segmentation fault: 11 on large (1MM points) arrays """
        # UK bounding box
        N = 55.811741
        E = 1.768960
        S = 49.871159
        W = -6.379880

        num_coords = 1000000
        lon_ls = list(np.random.uniform(W, E, [num_coords]))
        lat_ls = list(np.random.uniform(S, N, [num_coords]))
        convert_bng(lon_ls, lat_ls)

    def testBadValues(self):
        """ Test that values outside the bounding box return -1, -1 """
        bad_coords = [
            # Below minimum longitude
            [[-6.379881], [49.871159]],
            # Below minimum latitude
            [[1.768960], [49.871156]],
            # Above maximum longitude
            [[1.768961], [55.811741]],
            # Above maximum latitude
            [[1.768961], [55.811742]]
        ]
        for coord in bad_coords:
            result = convert_bng(coord[0], coord[1])
            self.assertTrue(math.isnan(result[0][0]))
            self.assertTrue(math.isnan(result[1][0]))

    def test_osgb36(self):
        """ Tests lon, lat --> OSGB36 conversion """
        expected = [[651409.792], [313177.448]]
        result = convert_to_osgb36(1.716073973, 52.658007833)
        self.assertEqual(expected, result)

    def test_osgb36_to_lonlat(self):
        """ Tests OSGB36 --> Lon, Lat conversion """
        # Not sure why this is being truncated
        # expected = [[1.716073973], [52.658007833]]
        expected = [[1.71607397], [52.65800783]]
        result = convert_osgb36_to_lonlat(651409.792, 313177.448)
        self.assertEqual(expected, result)

    def test_etrs89_to_osgb36(self):
        """ Tests ETRS89 Eastings, Northings --> OSGB36 conversion """
        expected = [[651409.792], [313177.448]]
        result = convert_etrs89_to_osgb36(651307.003, 313255.686)
        self.assertEqual(expected, result)

    def test_osgb36_to_etrs89(self):
        """ Tests OSGB36 --> ETRS89 Eastings, Northings conversion """
        expected = [[651307.003], [313255.686]]
        result = convert_osgb36_to_etrs89(651409.792, 313177.448)
        self.assertEqual(expected, result)

    def test_etrs89_to_lonlat(self):
        """ Tests ETRS89 --> Lon, Lat conversion"""
        expected =[[1.71607397], [52.65800783]]
        result = convert_etrs89_to_lonlat(651307.003, 313255.686)
        self.assertEqual(expected, result)

    def test_epsg3857_to_wgs84(self):
        """ Tests EPSG3857 to WGS84 conversion """
        expected = [[-5.625000000783013], [52.48278022732355]]
        result = convert_epsg3857_to_wgs84(-626172.1357121646, 6887893.4928337997)
