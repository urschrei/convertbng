import unittest
import numpy as np
from convertbng.convertbng.util import convertbng_list, convertlonlat_list, convertbng


class ConvertbngTests(unittest.TestCase):
    """ Tests for convertbng
    """

    def setUp(self):
        """ Set stuff up
        """
        pass

    def testConvertLonLat(self):
        """ Testing the threaded lon, lat --> BNG function """
        expected = [
            (516276L, 173141L),
            (398915L, 521545L),
            (604932L, 188804L),
            (574082L, 61931L),
            (523242L, 517193L),
            (515004L, 105661L),
            (566898L, 616298L)]
        result = convertbng_list([
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
        """ Testing the threaded BNG --> lon, lat function """

        expected = [
            (-0.328247994184494, 51.44533920288086),
            (-2.0183045864105225, 54.589115142822266),
            (0.95512455701828, 51.56087875366211),
            (0.44975531101226807, 50.43143081665039),
            (-0.09681292623281479, 54.535037994384766),
            (-0.36807215213775635, 50.83906555175781),
            (0.6348583698272705, 55.412208557128906)
        ]
        result = convertlonlat_list([
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

    def testLargeArrayConversion(self):
        """ Ensure that we don't get segmentation fault: 11 on large (1MM points) arrays """
        # UK bounding box
        N = 55.811741
        E = 1.768960
        S = 49.871159
        W = -6.379880

        num_coords = 1000000
        lon_ls = list(np.random.uniform(W, E, [num_coords]))
        lat_ls = list(np.random.uniform(S, N, [num_coords]))
        convertbng_list(lon_ls, lat_ls)
        

    def testConvertLonLatSingle(self):
        """ Ensure that the single lon, lat --> BNG function works """
        expected = (516276L, 173141L)
        result = convertbng(-0.32824866, 51.44533267)
        self.assertEqual(expected, result)
