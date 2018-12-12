"""utility funcs"""
#TODO: error collection

import math

def fmt_thou(val):
    """format a value with thousands seperator"""
    DEFAULT = '0'
    if val is None:
        return DEFAULT

    elif isinstance(val, float):
        if math.isnan(val):
            return DEFAULT

    return '{:,}'.format(round(val, 2))


def fmt_pct(val, pts):
    """assert that we have decimal pct and give it the required decimal points"""
    if isinstance(val, str):
        if '%' in val:
            return val

        else:
            try:
                val = float(val)
            except Exception:
                raise Exception('bad decimal for {0}'.format(val))

    if val > 1:
        raise Exception('bad decimal for {0}'.format(val))

    if math.isnan(val) or val == 0:
        return '0.{}%'.format('0'*pts)

    else:
        #can be done using decimal fmt?
        rnd = str(round(val * 100, pts))
        l_r = len(rnd.split('.')[1])

        if pts == 0:
            rnd = rnd.split('.')[0]

        elif l_r < pts:
            rnd += '0' * (pts - l_r)

        return '{0}{1}'.format(rnd, '%')


def nan_to_none(col):
    """set all NaNs to Nones in a list"""
    # TODO: better way?
    ret_l = []
    for v in col:
        if isinstance(v, float):
            if math.isnan(v):
                v = None

        ret_l.append(v)

    return ret_l


def clean_xls_headers(sht, num_cols):
    """strip #s from headers, remove unnecessary header cols"""
    sht = sht.rename(columns=lambda x: x.strip('#'))
    sht = sht.drop(sht.index[0:num_cols])
    return sht


def process_sht(sht):
    """run processing functions on sheet
        DONE:
        # set nans to None
        # rm #s from index

        TODO:
        # check to see if correct types in cols
        # merge with clean_xls_headers?


        in progress....
    """

    sht = sht.apply(lambda x : nan_to_none(x))
    return sht

def get_list_typo(in_vals, top, sort):
    """
    read in a list of tups of (type, pct_1, pct_2) and return top X sorted by 'sort', and then 1 - sum(rest) for "Others"
    """
    assert(len(set(len(v) for v in in_vals)) == 1)

    vals = sorted([[(v if i == 0 else 0 if v is None or math.isnan(v) else v) for i, v in enumerate(t)]
                   for t in in_vals], key = lambda x : x[sort], reverse=True)

    if len(vals) < top:
        ret = vals

    else:
        ret = []
        for v in vals[:top]:
            ret.append(v)

        mid = [0 for v in range(len(vals[1]) - 1)]
        for v in vals[top:]:
            for i in range(len(mid)):
                #+1 bc we're skipping one position of the index
                mid[i] += v[i+1]

        ret.append(['Others'] + mid)

    return ret