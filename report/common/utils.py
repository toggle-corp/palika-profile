"""utility funcs"""
#TODO: error collection
import math

import cairo
from hrrpmaps.atlas_auto import at

from report.common.boiler import get_lang

def swap_nep_chars(num):
    """swap in nepal numerical characters"""
    swap = { '0' : '०', '1' : '१', '2' : '२', '3' : '३', '4' : '४',
             '5' : '५', '6' : '६', '7' : '७', '8' : '८', '9' : '९' }
    return ''.join([swap[v] if v in swap else v for v in num])

def fmt_num(val):
    """properly format a number with the right thounsands seperation into eng or np
        remove decimals for all nums"""

    DEFAULT = '-'
    if val is None:
        return DEFAULT

    elif isinstance(val, float):
        if math.isnan(val):
            return DEFAULT

    v_str = str(round(val))
    fmtd = ''

    if get_lang() == 'np':
        #a bit hacky
        v_str = swap_nep_chars(v_str)
        COMM_PT = 2
        skip = ''

        if len(v_str) > 3:
            fmtd = ',' + v_str[-3:]
            v_str = v_str[:-3]

            if len(v_str) % 2 != 0:
                skip = v_str[0] + ',' if len(v_str) > 1 else v_str[0]
                v_str= v_str[1:]

            fmtd = skip + ','.join([v_str[i:i + COMM_PT] for i in range(0, len(v_str), COMM_PT)]) + fmtd
        else:
            fmtd = v_str

    else:
        fmtd = '{:,}'.format(round(val, 2))

    return fmtd


def fmt_pct(val, pts):
    """assert that we have decimal pct and give it the required decimal points"""
    ret = ''
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
        ret = '0.{}%'.format('0'*pts)

    else:
        #can be done using decimal fmt?
        rnd = str(round(val * 100, pts))
        l_r = len(rnd.split('.')[1])

        if pts == 0:
            rnd = rnd.split('.')[0]

        elif l_r < pts:
            rnd += '0' * (pts - l_r)

        ret = '{0}{1}'.format(rnd, '%')

    if get_lang() == 'np':
        ret = swap_nep_chars(ret)

    return ret


def nan_list_conv(col, r_v):
    """set all NaNs to r-v in a list"""
    # TODO: better way?
    ret_l = []
    for v in col:
        if isinstance(v, float):
            if math.isnan(v):
                v = r_v

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

    sht = sht.apply(lambda x : nan_list_conv(x, None))
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

def get_faq(faq_num, faq_sht, meta_sht):
    """get FAQ values. if no FAQ specified or invalid, go to default"""
    #TODO: collect error here for when invalid or not in list
    #TODO: Nep trans
    if faq_num not in faq_sht.index:
        faq_num = meta_sht.loc['Default FAQ']['value_en']

    return {'q': faq_sht.loc[faq_num]['question'], 'a': faq_sht.loc[faq_num]['answer']}

def gen_maps(pka_list, img_type):
    #TODO: error, check if the provided palika codes are actually in our data
    #TODO: delete once finished running

    print(get_lang())
    if get_lang() in ('en', 'np'):
        pka_style_lang = './resources/mapfiles/styles/palika_style_%s.qml' % get_lang()
    else:
        raise Exception('Bad language for map styling, bro.')

    atlas = at(
        data_uri='./resources/data/profile_data_structure_template.xlsx',
        wards_uri='./resources/mapfiles/hrrp_shapes/wards/merge.shp',
        palika_uri='./resources/mapfiles/hrrp_shapes/palika/GaPaNaPa_hrrp.shp',
        dists_uri='./resources/mapfiles/hrrp_shapes/districts/Districts_hrrp.shp',

        dists_syle='./resources/mapfiles/styles/dist_style.qml',
        pka_style=pka_style_lang,
        pka_hide_style='./resources/mapfiles/styles/palika_hide_style.qml',
        ward_style='./resources/mapfiles/styles/ward_style.qml',
        atlas_style='./resources/mapfiles/styles/atlas_layout.qpt',

        parent_join_cd='N_WCode',
        to_join_code='ward',
        pka_list=pka_list,
        img_type=img_type,

        out_path='./resources/mapfiles/map_tmp/')

    atlas.make_maps()

def get_text_width(text, fontsize, font, font_weight):
    """get width of text"""
    if font_weight.lower() == 'bold':
        font_weight = cairo.FONT_WEIGHT_BOLD
    elif font_weight.lower() == 'normal':
        font_weight = cairo.FONT_WEIGHT_NORMAL
    else:
        raise Exception ('font_weight must be in ("bold", "normal")')

    surface = cairo.SVGSurface(None, 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, font_weight)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
    return width