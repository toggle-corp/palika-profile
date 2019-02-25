"""utility funcs"""
# TODO: error collection
import math
import os
import copy
from collections import OrderedDict

import cairo
from hrrpmaps.atlas_auto import at

from ..common.boiler import get_lang, boil
from ..common import ZERO_DEFAULT


RESOURCES_DIR = os.path.abspath(
    os.path.join(
        os.path.join(os.path.abspath(__file__), '../../../'),
        'resources',
    )
)


def get_resource_abspath(resource_file):
    return os.path.join(RESOURCES_DIR, resource_file)


def swap_nep_chars(num):
    """swap in nepal numerical characters"""
    swap = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    return ''.join([swap[v] if v in swap else v for v in num])


def fmt_num(val):
    """properly format a number with the right thounsands seperation into eng or np
        remove decimals for all nums"""

    if val is None:
        return ZERO_DEFAULT

    elif isinstance(val, float):
        if math.isnan(val):
            return ZERO_DEFAULT

    # TODO: revert (swa_nep_chars command)
    # v_str = str(round(int(val)))

    fmtd = None

    if get_lang() == 'np':
        # a bit hacky
        v_str = swap_nep_chars(str(val))
        COMM_PT = 2
        skip = ''

        if len(v_str) > 3:
            fmtd = ',' + v_str[-3:]
            v_str = v_str[:-3]

            if len(v_str) % 2 != 0:
                skip = v_str[0] + ',' if len(v_str) > 1 else v_str[0]
                v_str = v_str[1:]

            fmtd = skip + ','.join(
                [
                    v_str[i:i + COMM_PT] for i in range(0, len(v_str), COMM_PT)
                 ]) + fmtd
        else:
            fmtd = v_str

    else:
        # TODO: revert
        fmtd = '{:,}'.format(round(int(val), 2))

    return fmtd


def fmt_pct(val, pts):
    """
    assert that we have decimal pct and give it the required decimal points
    """
    ret = ''
    if isinstance(val, str):
        if '%' in val:
            return val

        else:
            try:
                val = float(val)
            except Exception:
                raise Exception('bad decimal for {0}'.format(val))

    # if val > 1:
    #     #TODO: revert
    #     # raise Exception('bad decimal for {0}'.format(val))
    #     val/=100

    if val is None or val == 0:
        ret = '0.{}%'.format('0'*pts)

    else:
        # can be done using decimal fmt?
        rnd = str(round(val * 100, pts))
        # TODO: revert?
        if len(rnd.split('.')) > 1:
            l_r = len(rnd.split('.')[1])

            if pts == 0:
                rnd = rnd.split('.')[0]

            elif l_r < pts:
                rnd += '0' * (pts - l_r)

        ret = '{0}{1}'.format(rnd, '%')

    if get_lang() == 'np':
        ret = swap_nep_chars(ret)

    return ret


def get_list_typo(in_vals, top):
    """
    read in a list of tups of (type, pct_1, pct_2) and return:
        [valid entries meaning not 0]
        top X sorted by 'sort' in pct_1 until we reach 0 or if the len of valid
        entries >=top, display 1-sum(other)
        if len valid entries < top, start showing for pct_2
            if len valid entries for pct_1 + pct_2 >= top, display 1-sum(other)
            if len valid entries for pct_1 + pct_2 is still < top, only do that
            many rows

    input: [{'key' : x, 'muni_pct' : y, 'dist_pct' : z}]
    """

    # TODO: hacky method
    FRST_COL = 'muni_pct'
    SCND_COL = 'dist_pct'
    out_vals = OrderedDict()

    for k, v in in_vals.items():
        in_vals[k] = {
            ik: 0 if iv is None or is_nan(iv) else iv for ik, iv in v.items()
        }

    in_vals = OrderedDict(
        sorted(in_vals.items(), key=lambda x: x[1][FRST_COL], reverse=True)
    )

    def _sum_grp(col):
        # sum group in in_vals for appropriate col and pop applied values

        tmp_it = copy.copy(in_vals)
        for i, v in enumerate(tmp_it.items()):
            it = list(tmp_it.items())[i]
            if i == top-1 or v[1][col] <= 0:
                break

            else:
                out_vals[it[0]] = it[1]
                in_vals.pop(v[0])

        return in_vals, out_vals, sum([v[1][col] for v in in_vals.items()])

    # handle first col
    in_vals, out_vals, rem_sum = _sum_grp(FRST_COL)
    top -= len(out_vals)-1

    # add sum if there are still first col values, otherwise move to second col
    if rem_sum > 0:
        out_vals[boil('typologies_others')] = {
            FRST_COL: rem_sum,
            SCND_COL: sum([v[1][SCND_COL] for v in in_vals.items()])
        }

    else:
        # handle second col
        in_vals = OrderedDict(
            sorted(
                in_vals.items(), key=lambda x: x[1][SCND_COL], reverse=True,
            ),
        )
        in_vals, out_vals, rem_sum = _sum_grp(SCND_COL)
        if rem_sum > 0:
            out_vals[boil('typologies_others')] = {
                FRST_COL: 0,
                SCND_COL: sum([v[1][SCND_COL] for v in in_vals.items()]),
            }

    return out_vals


def get_faq(faq_num, faq_sht, meta_sht):
    """get FAQ values. if no FAQ specified or invalid, go to default"""
    # TODO: collect error here for when invalid or not in list
    # TODO: Nep trans
    if faq_num not in faq_sht.index:
        faq_num = meta_sht.loc['Default FAQ']['value_en']

    return {
        'q': faq_sht.loc[faq_num]['question'],
        'a': faq_sht.loc[faq_num]['answer'],
    }


def gen_maps(pka_list, img_type):
    # TODO: error, check if the provided palika codes are actually in our data
    # TODO: delete once finished running

    print(get_lang())
    if get_lang() in ('en', 'np'):
        pka_style_lang = get_resource_abspath('mapfiles/styles/palika_style_%s.qml' % get_lang()) # noqa
    else:
        raise Exception('Bad language for map styling, bro.')

    atlas = at(
        data_uri=get_resource_abspath('data/profile_data_structure_template.xlsx'), # noqa
        wards_uri=get_resource_abspath('mapfiles/hrrp_shapes/wards/merge.shp'),
        palika_uri=get_resource_abspath('mapfiles/hrrp_shapes/palika/GaPaNaPa_hrrp.shp'), # noqa
        dists_uri=get_resource_abspath('mapfiles/hrrp_shapes/districts/Districts_hrrp.shp'), # noqa

        dists_syle=get_resource_abspath('mapfiles/styles/dist_style.qml'),
        pka_style=pka_style_lang,
        pka_hide_style=get_resource_abspath('mapfiles/styles/palika_hide_style.qml'), # noqa
        ward_style=get_resource_abspath('mapfiles/styles/ward_style.qml'),
        atlas_style=get_resource_abspath('mapfiles/styles/atlas_layout.qpt'),

        parent_join_cd='N_WCode',
        to_join_code='ward',
        pka_list=pka_list,
        img_type=img_type,

        out_path=get_resource_abspath('mapfiles/map_tmp/')
    )

    atlas.make_maps()


def get_text_width(text, fontsize, font, font_weight):
    """get width of text"""
    if font_weight.lower() == 'bold':
        font_weight = cairo.FONT_WEIGHT_BOLD
    elif font_weight.lower() == 'normal':
        font_weight = cairo.FONT_WEIGHT_NORMAL
    else:
        raise Exception('font_weight must be in ("bold", "normal")')

    surface = cairo.SVGSurface(None, 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, font_weight)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(
        text,
    )
    return width


def is_nan(val):
    try:
        if math.isnan(val):
            return True
    except: # noqa
        pass
    return False
