import unittest
import math
from collections import OrderedDict

from report.common import boiler, utils
from report.common.Sheet import Sheet
from report.common.boiler import strings
from report.page2 import hh

import numpy as np
import pandas as pd


# TODO: break up into seperate test files
class Tests(unittest.TestCase):
    def setUp(self):
        boiler.set_lang('en')
        strings['typologies_others'] = {'en' : 'Others'}

        # hh
        self.hh_test_data = {
            'v1': 10,
            'v2': None,
            'v3': 0,
            'v4': np.NaN,
            'v5': 20,
            'v6': 1000
        }
        self.hh_test_filt_res = \
            [{'key': 'v1', 'val': 10},
             {'key': 'v5', 'val': 20},
             {'key': 'v6', 'val': 1000}]

    ####report.common.boiler
    def test_trans_blank(self):
        res = boiler.boil('not included')
        self.assertEqual(res, '***VALUE NOT IN XLS***')

    ####hh
    def test_get_widths(self):
        res = [{'key': 'v1', 'val': 10, 'w': 18},
               {'key': 'v5', 'val': 20, 'w': 18},
               {'key': 'v6', 'val': 1000, 'w': 600}]
        # self.assertEqual(hh._get_widths(self.hh_test_filt_res), res)

    def test_filter_items(self):
        items = [{'key': 'v%i' % i} for i in range(1, 7)]
        self.assertEqual(hh._filter_items(items, self.hh_test_data), self.hh_test_filt_res)

    ####report.common.Sheet
    def test_nan_conv(self):
        test_sht = Sheet(pd.DataFrame([1, math.nan, 'test'], columns=['test']))
        self.assertEqual(test_sht.nan_list_conv('test', None), [1, None, 'test'])

    def test_clean_int(self):
        col_nm = 'test'
        test_sht = Sheet(pd.DataFrame([1, '3', 2.5, math.nan, 'test'], columns=[col_nm]))
        self.assertEqual(test_sht._clean_int(col_nm, test_sht.sht[col_nm]), [1, 3, 2, None, None])

    def test_clean_str(self):
        col_nm = 'test'
        test_sht = Sheet(pd.DataFrame(['xx', 2.5, math.nan, ''], columns=[col_nm]))
        self.assertEqual(test_sht._clean_str(col_nm, test_sht.sht[col_nm]),
                         ['xx', '2.5', None, ''])

    def test_clean_dec(self):
        col_nm = 'test'
        test_sht = Sheet(pd.DataFrame(['xx', 2.5, math.nan, .8, '.1', 1, 0], columns=[col_nm]))
        self.assertEqual(test_sht._clean_dec(col_nm, test_sht.sht[col_nm]),
                         [None, 2.5, None, .8, .1, 1, 0])

    def test_clean_pct(self):
        col_nm = 'test'
        test_sht = Sheet(pd.DataFrame(['xx', 2.5, math.nan, .8, '.1', 1, 0], columns=[col_nm]))
        self.assertEqual(test_sht._clean_pct(col_nm, test_sht.sht[col_nm]),
                         [None, None, None, .8, .1, 1, 0])

    def test_clean_uid_missing(self):
        col_nm = 'test'
        test_sht = Sheet(pd.DataFrame([], columns=[col_nm],
                                      index = [1, 2, 3, 4, math.nan]))
        test_sht._clean_uid(col_nm, list(test_sht.sht.index))
        self.assertEqual(len(test_sht.errors), 1)

    def test_clean_uid_rep(self):
        col_nm = 'test'
        test_sht = Sheet(pd.DataFrame([1, 2, 3, 4, 4], columns=[col_nm]))
        test_sht._clean_uid(col_nm, test_sht.sht[col_nm])
        self.assertEqual('Duplicate UID values detected',
                         test_sht.errors[0]['message'])

    ####report.commons.utils
    def test_decimal_prop(self):
        self.assertEqual(utils.fmt_pct(0.5, 2), '50.00%')
        self.assertEqual(utils.fmt_pct(0.5, 0), '50%')
        self.assertEqual(utils.fmt_pct(0.50, 2), '50.00%')
        self.assertEqual(utils.fmt_pct(0.510, 2), '51.00%')
        self.assertEqual(utils.fmt_pct(0.5123, 2), '51.23%')
        self.assertEqual(utils.fmt_pct(0.512312342, 2), '51.23%')

    def test_list_typo_all_muni(self):
        l = OrderedDict()
        l['v'] = {'muni_pct' : None, 'dist_pct' : 1}
        l['v2'] = {'muni_pct' : 2, 'dist_pct' : None}
        l['v3'] = {'muni_pct' : None, 'dist_pct' : 4}
        l['v4'] = {'muni_pct' : 200, 'dist_pct' : 5}
        l['v5'] = {'muni_pct' : None, 'dist_pct' : 1}
        l['v6'] = {'muni_pct' : 20, 'dist_pct' : 2}
        l['v7'] = {'muni_pct' : 15, 'dist_pct' : 3}
        l['v8'] = {'muni_pct' : 15, 'dist_pct' : 5}
        l['v9'] = {'muni_pct' : 10, 'dist_pct' : 6}
        l['v11'] = {'muni_pct' : 9, 'dist_pct' : 1}
        l['v12'] = {'muni_pct' : 9, 'dist_pct' : 1}

        res = OrderedDict()
        res['v4'] = {'muni_pct': 200, 'dist_pct': 5}
        res['v6'] = {'muni_pct': 20, 'dist_pct': 2}
        res['v7'] = {'muni_pct': 15, 'dist_pct': 3}
        res['v8'] = {'muni_pct': 15, 'dist_pct': 5}
        res['v9'] = {'muni_pct': 10, 'dist_pct': 6}
        res['Others'] = {'muni_pct': 20, 'dist_pct': 8}

        self.assertEqual(utils.get_list_typo(l, 6), res)

    def test_list_typo_short_pct1_enough_pct2(self):
        l = OrderedDict()
        l['v4'] = {'muni_pct' :  200, 'dist_pct' : 5}
        l['v6'] = {'muni_pct' :  20, 'dist_pct' : 2}
        l['v7'] = {'muni_pct' :  15, 'dist_pct' : 3}
        l['v'] = {'muni_pct' :  None, 'dist_pct' : 1}
        l['v2'] = {'muni_pct' :  None, 'dist_pct' : 4}
        l['v3'] = {'muni_pct' :  None, 'dist_pct' : 4}
        l['v5'] = {'muni_pct' :  None, 'dist_pct' : 1}

        res = OrderedDict()
        res['v4'] = {'muni_pct': 200, 'dist_pct': 5}
        res['v6'] = {'muni_pct': 20, 'dist_pct': 2}
        res['v7'] = {'muni_pct': 15, 'dist_pct': 3}
        res['v2'] = {'muni_pct': 0, 'dist_pct': 4}
        res['v3'] = {'muni_pct': 0, 'dist_pct': 4}
        res['Others'] = {'muni_pct': 0, 'dist_pct': 2}

        self.assertEqual(utils.get_list_typo(l, 5), res)

    def test_list_typo_short_pct1_exact_pct2(self):
        l = OrderedDict()
        l['v4'] = {'muni_pct' :  200, 'dist_pct' : 5}
        l['v6'] = {'muni_pct' :  20, 'dist_pct' : 2}
        l['v7'] = {'muni_pct' :  15, 'dist_pct' : 3}
        l['v'] = {'muni_pct' :  None, 'dist_pct' : 1}
        l['v2'] = {'muni_pct' :  None, 'dist_pct' : 4}

        res = OrderedDict()
        res['v4'] = {'muni_pct': 200, 'dist_pct': 5}
        res['v6'] = {'muni_pct': 20, 'dist_pct': 2}
        res['v7'] = {'muni_pct': 15, 'dist_pct': 3}
        res['v2'] = {'muni_pct': 0, 'dist_pct': 4}
        res['v'] = {'muni_pct': 0, 'dist_pct': 1}

        self.assertEqual(utils.get_list_typo(l, 5), res)

    def test_list_typo_bad_len(self):
        pass
        # TODO: func call?
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
        self.assertEqual(utils.get_list_typo(l, 5), [['v2', 2], ['v', 0]])

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
