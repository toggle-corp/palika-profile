import unittest
import math

from report.common import boiler, utils
from report.page2 import hh

import numpy as np


class Tests(unittest.TestCase):

    def setUp(self):
        self.hh_test_data = {
            'v1': 10,
            'v2': None,
            'v3': 0,
            'v4': np.NaN,
            'v5': 20,
            'v6': 1000
        }
        self.hh_test_filt_res = \
            [{'key' : 'v1', 'val' : 10},
               {'key' : 'v5', 'val' : 20},
               {'key' : 'v6', 'val' : 1000}]

        boiler.set_lang('en')

    ####boil
    def test_trans_blank(self):
        res = boiler.boil('not included')
        self.assertEqual(res, '***VALUE NOT IN XLS***')

    ####hh
    def test_get_widths(self):
        res = [{'key' : 'v1', 'val' : 10, 'w' : 18},
               {'key' : 'v5', 'val' : 20, 'w' : 18},
               {'key' : 'v6', 'val' : 1000, 'w' : 600}]
        # self.assertEqual(hh._get_widths(self.hh_test_filt_res), res)

    def test_filter_items(self):
        items = [{'key' : 'v%i' % i} for i in range(1,7)]
        self.assertEqual(hh._filter_items(items, self.hh_test_data), self.hh_test_filt_res)

    ####report.commons.utils
    def test_nan_conv(self):
        self.assertEqual(utils.nan_list_conv([1, math.nan, 'test'], None), [1, None, 'test'])

    def test_decimal_prop(self):
        self.assertEqual(utils.fmt_pct(0.5, 2), '50.00%')
        self.assertEqual(utils.fmt_pct(0.5, 0), '50%')
        self.assertEqual(utils.fmt_pct(0.50, 2), '50.00%')
        self.assertEqual(utils.fmt_pct(0.510, 2), '51.00%')
        self.assertEqual(utils.fmt_pct(0.5123, 2), '51.23%')
        self.assertEqual(utils.fmt_pct(0.512312342, 2), '51.23%')

    def test_list_typo(self):
        l = [
                ('v', None, 1, 10),
                ('v2', 2, None, 34),
                ('v3', None, 4, 5),
                ('v4', 200, 5, 2),
                ('v5', None, 1, 3),
                ('v6', 20, 2, 256),
                ('v7', 15, 3, 4),
                ('v8', 15, 5, 322),
                ('v9', 10, 6, 13),
                ('v11', 9, 1, 3),
                ('v12', 9, 1, 4),
        ]
        self.assertEqual(utils.get_list_typo(l, 5, 1),
                         [['v4', 200, 5, 2], ['v6', 20, 2, 256], ['v7', 15, 3, 4], ['v8', 15, 5, 322],
                          ['v9', 10, 6, 13], ['Others', 20, 8, 59]])

    def test_list_typo_bad_len(self):
        pass
        #TODO: func call?
        # l = [(1), (1, 2)]
        #
        # with self.assertRaises(AssertionError) as cm:
        #     utils.get_list_typo(l, 5)
        #
        # the_exception = cm.exception
        # self.assertEqual(the_exception.error_code, AssertionError)

    def test_list_typo_short(self):
        l = [
                ('v', None),
                ('v2', 2)
            ]
        self.assertEqual(utils.get_list_typo(l, 5, 1), [['v2', 2], ['v', 0]])

    def test_fmt_num_np(self):
        "get num back like 1,23,45,67,890"
        boiler.set_lang('np')
        self.assertEqual(utils.fmt_num(123), '१२३')
        self.assertEqual(utils.fmt_num(1234), '१,२३४')
        self.assertEqual(utils.fmt_num(12345), '१२,३४५')
        self.assertEqual(utils.fmt_num(123456789), '१२,३४,५६,७८९')
        self.assertEqual(utils.fmt_num(3123456789), '३,१२,३४,५६,७८९')
        self.assertEqual(utils.fmt_num(31234567890), '३१,२३,४५,६७,८९०')

    def test_swap(self):
        self.assertEqual(utils.swap_nep_chars('1,234.00%'), '१,२३४.००%')


if __name__ == '__main__':
    unittest.main()
