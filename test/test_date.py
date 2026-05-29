import unittest

from tools.treatment_response import treatment_date


class TestDateMethod(unittest.TestCase):

    def test_date_reverse(self):
        date = " LE DIX HUIT JUIN L'AN DEUX MILLE DIX NEUF, "
        wait_result = "18/06/2019"
        result = treatment_date(date)
        self.assertEqual(wait_result, result)

    def test_date_reverse_without_year(self):
        date = " LE DIX HUIT JUIN DEUX MILLE DIX NEUF, "
        wait_result = "18/06/2019"
        result = treatment_date(date)
        self.assertEqual(wait_result, result)

    def test_date(self):
        date = "L'AN DEUX MILLE DIX NEUF, LE DIX HUIT JUIN "
        wait_result = "18/06/2019"
        result = treatment_date(date)
        self.assertEqual(wait_result, result)

    def test_date_mil_neuf_cent(self):
        date = "L'AN MILLE NEUF CENT QUATRE VINGT DIX NEUF, LE DIX HUIT JUIN "
        wait_result = "18/06/1999"
        result = treatment_date(date)
        self.assertEqual(wait_result, result)

    def test_date_mil_neuf_cent_reverse(self):
        date = "LE DIX HUIT JUIN L'AN MILLE NEUF CENT QUATRE VINGT DIX NEUF"
        wait_result = "18/06/1999"
        result = treatment_date(date)
        self.assertEqual(wait_result, result)

    def test_date_with_deux_deux(self):
        date = "DEUX JUIN DEUX MIL DIX NEUF"
        wait_result = "02/06/2019"
        result = treatment_date(date)
        self.assertEqual(wait_result, result)

    def test_date_error_tnr_1(self):
        date = "DEUX MIL DOUZE LE DIX JANVIER"
        wait_result = "10/01/2012"
        result = treatment_date(date)
        self.assertEqual(wait_result, result)

    def test_date_no_day(self):
        date = "DEUX MILLE VINGT-TROIS, Le"
        wait_result = "00/00/2023"
        result = treatment_date(date)
        self.assertEqual(wait_result, result)

    def test_date_no_le(self):
        date = "SIX JUILLET L'AN DEUX MILLE DIX SEPT"
        wait_result = "06/07/2017"
        result = treatment_date(date)
        self.assertEqual(wait_result, result)


if __name__ == '__main__':
    unittest.main()
