import unittest
from convertbng.convertbng.util import convertbng_list


class ConvertbngTests(unittest.TestCase):
    """ Tests for pyzotero
    """

    def setUp(self):
        """ Set stuff up
        """
        pass

    def testConvertList(self):
        """ Ensure that threaded vector function returns correct values
        """
        expected = [
            (516276L, 173141L),
            (398915L, 521545L),
            (604932L, 188805L),
            (574082L, 61932L),
            (523242L, 517194L),
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
