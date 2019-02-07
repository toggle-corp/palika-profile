"""various funcs for cleaning input data"""
import math
import os

from report.common.boiler import import_titles
from report.common import XLS_URI, SHT_RESERVE_CHAR
from report.common.utils import is_nan

import pandas as pd


# TODO: do pandas DF creation in init? ie for data clean
# TODO: collate errors
class Sheet(object):
    def __init__(self, sht, skip = None, test_len = None, overwrite = None, OUTPUT_PATH = None, lang_in = None,
                 num_rows_strip=0, remove_reserve_dims=None, reserve_val=None, process_specific=None):

        self.sht = sht
        self.num_rows_strip = num_rows_strip
        self.remove_reserve_dims = remove_reserve_dims
        self.reserve_val = reserve_val
        self.process_specific = process_specific
        self.errors = []

        # data sheet specific
        self.skip = skip
        self.test_len = test_len
        self.overwrite = overwrite
        self.OUTPUT_PATH = OUTPUT_PATH
        self.lang_in = lang_in

    def process(self):
        self.clean_headers()

        if self.process_specific == 'data':
            self.types = Sheet(
                pd.read_excel(XLS_URI, sheet_name = 'data_types', header = 0, index_col=0),
                remove_reserve_dims=['rows', 'columns'], reserve_val=SHT_RESERVE_CHAR)
            self.types.process()
            self._process_data()

        elif self.process_specific == 'titles':
            self._process_titles()

    def _process_titles(self):
        """do special processing for titles sheet"""
        import_titles(self.sht)

    def clean_headers(self):
        """strip #s from headers, remove unnecessary header cols"""
        if self.remove_reserve_dims:
            for v in self.remove_reserve_dims if isinstance(self.remove_reserve_dims, list) \
                    else [self.remove_reserve_dims]:

                if v == 'rows':
                    self.sht.rename(lambda x: str(x).strip('#'), axis='rows', inplace=True)
                elif v == 'columns':
                    self.sht = self.sht.rename(columns=lambda x: str(x).strip('#'))
                else:
                    raise Exception('Bad dims type for {}. Must be "rows" or "columns"'.format(v))

        if self.num_rows_strip > 0:
            self.sht = self.sht.drop(self.sht.index[0:self.num_rows_strip])

    ### data processing
    def _process_data(self):
        """run cleaning functions on data sheet

        data types cleaned:
        int: gets rounded down
        str: read as string
        dec: accept decimal value if it is present - cap @ 2 places
        pct: must be <= 1, add in ‘% when displaying
        for all: if the value is nan, set to None

            DONE:
            # set nans to None
            # rm #s from index

            TODO:
            # check to see if correct types in cols
            # merge with clean_xls_headers?


            in progress....
        """
        # TODO: use apply, while passing index and col?
        # TODO: object type for cleaning? #yolo? #yoco?
        # TODO: not show string 'nan' for empties in error
        # iterate through each column and apply cleaning functions. Index is the name of the col in data sheet
        for v in self.types.sht.itertuples():
            if v.type == 'int':
                self.sht[v.Index] = self._clean_int(v.Index, self.sht[v.Index])
            elif v.type == 'str':
                self.sht[v.Index] = self._clean_str(v.Index, self.sht[v.Index])
            elif v.type == 'dec':
                self.sht[v.Index] = self._clean_dec(v.Index, self.sht[v.Index])
            elif v.type == 'pct':
                self.sht[v.Index] = self._clean_pct(v.Index, self.sht[v.Index])
            elif v.type == 'uid':
                #UIDs are indexes, and are coerced to being strings if they're not
                self.sht.index = self._clean_uid(v.Index, list(self.sht.index))
            else:
                raise Exception('Bad item type for type {}. Must be in (int, str, dec, pct, uid). '
                                'Did you change something in the data_types sheet?'.format(v))

        self._trim_data()

    def _trim_data(self):
        # drop specified list
        self.sht.drop([str(v) for v in self.skip], axis = 'index', errors = 'ignore', inplace = True)

        # trim to appropriate length
        self.sht = self.sht[:self.test_len] if self.test_len else self.sht

        # remove files we don't want to overwrite
        if not self.overwrite:
            rm_over = list(set([v.split('_')[0] for v in os.listdir(self.OUTPUT_PATH) if '_{}.pdf'.format(self.lang_in) in v])
                           & set(self.sht.index.values))

            print('Not overwriting: ', sorted(rm_over))
            self.sht.drop(rm_over, axis = 'index', inplace = True)

    def _clean_int(self, col_nm, srs):
        """apply int cleaning functions to a pd Series PANDAS PANDAS PANDAS PANDAS
        INPUT: PANDAS
        OUTPUT: MUSHROOM MUSHROOM
        raise Exception("IT'S A SNAKE!!!")
        """
        ERR_STR = 'Bad integer value for {}'
        col = []
        for ind, v in srs.iteritems():
            try:
                #TODO: warn on decimal convert
                col.append(int(v))
            except:
                self._add_error(message=ERR_STR.format(str(v)), column=col_nm, index=ind)
                col.append(None)

        return col

    def _clean_uid(self, col_nm, srs):
        """apply int cleaning functions to a pd Series PANDAS PANDAS PANDAS PANDAS
        INPUT: PANDAS
        OUTPUT: MUSHROOM MUSHROOM
        raise Exception("IT'S A SNAKE!!!")
        """
        ERR_STR = 'Bad integer value for {}'
        col = []


    def nan_list_conv(self, col, r_v):
        """set all NaNs to r_v in a list"""
        # TODO: better way?
        ret_l = []
        for v in self.sht[col]:
            if isinstance(v, float):
                if math.isnan(v):
                    v = r_v

            ret_l.append(v)

        return ret_l

    def _clean_str(self, col_nm, srs):
        """apply str cleaning functions to a pd Series"""
        ERR_STR = 'Bad string value for {}'
        col = []
        for ind, v in srs.iteritems():
            try:
                if is_nan(v):
                    col.append(None)
                else:
                    col.append(str(v))
            except:
                self._add_error(message=ERR_STR.format(str(v)), column=col_nm, index=ind)
                col.append(None)

        return col

    def _clean_dec(self, col_nm, srs):
        """apply dec cleaning functions to a pd Series"""
        ERR_STR = 'Bad decimal value for {}'
        col = []
        for ind, v in srs.iteritems():
            try:
                if is_nan(v):
                    col.append(None)
                else:
                    col.append(float(v))
            except:
                self._add_error(message=ERR_STR.format(str(v)), column=col_nm, index=ind)
                col.append(None)

        return col

    def _clean_pct(self, col_nm, srs):
        """apply pct cleaning functions to a pd Series"""
        ERR_STR = 'Bad pct value for {}. Value must be less than 1.'
        col = []
        for ind, v in srs.iteritems():
            try:
                if float(v) > 1 or is_nan(v):
                    col.append(None)
                else:
                    col.append(float(v))
            except:
                self._add_error(message=ERR_STR.format(str(v)), column=col_nm, index=ind)
                col.append(None)

        return col

    def _clean_uid(self, col_nm, idx_vals):
        """apply uid cleaning functions to a list of indices. check if nan, and then if any repeats"""

        #TODO: list repeats?
        if len(idx_vals) != len(set(idx_vals)):
            self._add_error(message='Duplicate UID values detected', column=col_nm, index='N/A')

        col = []
        for v in idx_vals:
            if is_nan(v):
                self._add_error(message='Bad UID value for {}. It is blank and is being skipped.'
                                .format(str(v)), column=col_nm, index='Missing')
            else:
                col.append(str(v))

        #TODO: list repeats?
        if len(idx_vals) != len(set(idx_vals)):
            self._add_error(message='Duplicate UID values detected', column=col_nm, index='N/A')

        return col

    def _add_error(self, message, index=None, column=None):
        """create error log for data in excel sheet.
            index: index where error occurred
            column: column where error occurred
            message: description of error
        """
        self.errors.append(dict(message=message, index=index, column=column))