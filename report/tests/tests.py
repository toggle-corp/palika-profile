import unittest
import math

from report.common import boiler, utils


class Tests(unittest.TestCase):

    ####trans
    def test_trans_blank(self):
        res = boiler.get('not included')
        self.assertEqual(res, '***VALUE NOT IN XLS***')

    def test_trans_ok(self):
        res = boiler.set('t,', 'fine')
        self.assertEqual('fine', boiler.get('t'))

    ####report.commons.utils
    def test_nan_non(self):
        self.assertEqual(utils.nan_to_none([1, math.nan, 'test']), [1, None, 'test'])

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
        self.assertEqual(utils.fmt_num(1234), '१,२३४')
        self.assertEqual(utils.fmt_num(12345), '१२,३४५')
        self.assertEqual(utils.fmt_num(123456789), '१२,३४,५६,७८९')
        self.assertEqual(utils.fmt_num(3123456789), '३,१२,३४,५६,७८९')
        self.assertEqual(utils.fmt_num(31234567890), '३१,२३,४५,६७,८९०')

    def test_swap(self):
        self.assertEqual(utils.swap_nep_chars('1,234.00%'), '१,२३४.००%')


if __name__ == '__main__':
    unittest.main()
