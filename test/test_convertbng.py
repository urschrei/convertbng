import unittest
import numpy as np
import array
from convertbng.convertbng.util import (
    convertbng,
    convertlonlat,
    convert_osgb36,
    convert_osgb36_to_lonlat,
    convert_osgb36_to_etrs89,
    convert_etrs89_to_osgb36,
    convert_etrs89_to_ll,
    convert_epsg3857_to_wgs84
)

from ctypes import ArgumentError


class ConvertbngTests(unittest.TestCase):
    """ Tests for convertbng
    """

    def setUp(self):
        """ Set stuff up
        """
        pass

    def testConvertLonLat(self):
        """ Test multithreaded lon, lat --> BNG function """
        expected = [
            [516275.973, 398915.033, 604931.645, 574082.246, 523242.007, 515004.123, 566898.408],
            [173141.092, 521545.067, 188804.36, 61931.28, 517193.249, 105660.976, 616298.251]
        ]
        result = convertbng([
            -0.32824866,
            -2.0183041005533306,
            0.95511887434519682,
            0.44975855518383501,
            -0.096813621191803811,
            -0.36807065656416427,
            0.63486335458665621],
        [
            51.44533267,
            54.589097162646141,
            51.560873800587828,
            50.431429161121699,
            54.535021436247419,
            50.839059313135706,
            55.412189281234419])
        self.assertEqual(expected, result)

    def testConvertBNG(self):
        """ Test multithreaded BNG --> lon, lat function """
        expected = [
            [-0.32824799, -2.01830465, 0.95512453, 0.44975531, -0.09681292, -0.36807217, 0.63485837],
            [51.44534027, 54.58911602, 51.56087908, 50.43143151, 54.53503836, 50.83906588, 55.41220958]
        ]
        result = convertlonlat([
            516276L,
            398915L,
            604932L,
            574082L,
            523242L,
            515004L,
            566898L],
        [
            173141L,
            521545L,
            188804L,
            61931L,
            517193L,
            105661L,
            616298L])
        self.assertEqual(expected, result)

    def testConvertLonLatSingle(self):
        """ Test lon, lat --> BNG conversion of single values """
        expected = [[516275.973], [173141.092]]
        result = convertbng(-0.32824866, 51.44533267)
        self.assertEqual(expected, result)

    def testConvertTuple(self):
        """ Test lon, lat --> BNG conversion of tuples """
        expected = [[516275.973], [173141.092]]
        result = convertbng((-0.32824866,), (51.44533267,))
        self.assertEqual(expected, result)

    def testConvertString(self):
        """ Test that an error is thrown for incorrect types """
        with self.assertRaises(ArgumentError) as result:
            convertbng(['Foo'], ['Bar'])

    def testConvertIterable(self):
        """ Test lon, lat --> BNG conversion of tuples """
        expected = [[516275.973], [173141.092]]
        result = convertbng(iter([-0.32824866]), iter([51.44533267]))
        self.assertEqual(expected, result)

    def testConvertArray(self):
        """ Test lon, lat --> BNG conversion of array.array """
        expected = [[516275.977], [173140.97]]
        result = convertbng(array.array('f', [-0.32824866]), array.array('f', [51.44533267]))
        self.assertEqual(expected, result)

    def testGenerator(self):
        """ Test that the lon, lat -> BNG function can consume generators """
        expected = [
            [516275.973, 398915.033, 604931.645, 574082.246, 523242.007, 515004.123, 566898.408],
            [173141.092, 521545.067, 188804.36, 61931.28, 517193.249, 105660.976, 616298.251]
        ]
        inp = [
            [-0.32824866,
                -2.0183041005533306,
                0.95511887434519682,
                0.44975855518383501,
                -0.096813621191803811,
                -0.36807065656416427,
                0.63486335458665621],
            [51.44533267,
                54.589097162646141,
                51.560873800587828,
                50.431429161121699,
                54.535021436247419,
                50.839059313135706,
                55.412189281234419]
        ]
        lon_generator = (n for n in inp[0])
        lat_generator = (n for n in inp[1])
        result = convertbng(lon_generator, lat_generator)
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
        convertbng(lon_arr, lat_arr)
        
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
        convertbng(lon_ls, lat_ls)

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
            self.assertEqual([[9999], [9999]], convertbng(coord[0], coord[1]))

    def test_osgb36(self):
        """ Tests lon, lat --> OSGB36 conversion """
        expected = [[651409.792], [313177.448]]
        result = convert_osgb36(1.716073973, 52.658007833)
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

    def test_etrs89_to_osgb36(self):
        """ Tests OSGB36 --> ETRS89 Eastings, Northings conversion """
        expected = [[651307.003], [313255.686]]
        result = convert_osgb36_to_etrs89(651409.792, 313177.448)
        self.assertEqual(expected, result)

    def test_etrs89_to_lonlat(self):
        """ Tests ETRS89 --> Lon, Lat conversion"""
        expected =[[1.71607397], [52.65800783]]
        result = convert_etrs89_to_ll(651307.003, 313255.686)
        self.assertEqual(expected, result)

    def test_epsg3857_to_wgs84(self):
        """ Tests EPSG3857 to WGS84 conversion """
        expected = [[-5.625000000783013], [52.48278022732355]]
        result = convert_epsg3857_to_wgs84(-626172.1357121646, 6887893.4928337997)
