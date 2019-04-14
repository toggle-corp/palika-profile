"""utility funcs"""
# TODO: error collection
import math
import os
import copy
from collections import OrderedDict

import cairo
from hrrpmaps.atlas_auto import at

from ..common.boiler import get_lang, boil, boil_header
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
        v_str = swap_nep_chars(str(int(val)))
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
        fmtd = '{:,}'.format(round(int(val), 2))

    return fmtd


def fmt_dec(val, pts, dec=False):
    """convert values to decimal format with specified number of decimals.
        dec used for pct conversion.
    """
    try:
        val = float(val)
        if dec:
            val *= 100

    except Exception:
        print('in')
        # TODO: error handler

        print('bad decimal for {0}, converting to blank'.format(val))
        return ZERO_DEFAULT

    if is_nan(val):
        return ZERO_DEFAULT

    else:
        fmtd = '{:.{}f}'.format(val, pts)
        return fmtd if get_lang() != 'np' else swap_nep_chars(fmtd)


def fmt_pct(val, pts):
    """
    assert that we have decimal pct and give it the required decimal points
    """
    if isinstance(val, str):
        if '%' in val:
            return val

    if val > 1:
        # TODO: error handler
        # raise Exception('Decimal value is greater than 1: {0}'.format(val))
        # val/=100
        print('Decimal value is greater than 1: {0}'.format(val))

    ret = fmt_dec(val, pts, True)

    if val is None or val == 0:
        ret = '0.{}%'.format('0'*pts)

    else:
        ret = '{0}{1}'.format(fmt_dec(val, pts, True), '%')

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


def get_faq(faq_num, faq_sht):
    """get FAQ values. if no FAQ specified or invalid, go to default"""
    # TODO: collect error here for when invalid or not in list
    if faq_num not in faq_sht.index:
        faq_num = boil('faq_num')

    return {
        'q': faq_sht.loc[faq_num][boil_header('question', override = True)],
        'a': faq_sht.loc[faq_num][boil_header('answer', override = True)],
    }


def gen_maps(
        pka_list, img_type,
        # Shapes
        wards_uri=None, palika_uri=None, dists_uri=None,
        # Styles
        dists_style_uri=None, pka_hide_style_uri=None, atlas_style_uri=None,
        ward_style_uri=None, pka_style_lang_uri=None,
):
    # TODO: error, check if the provided palika codes are actually in our data
    # TODO: delete once finished running

    if get_lang() in ('en', 'np'):
        pka_style_lang = get_resource_abspath('mapfiles/styles/palika_style_%s.qml' % get_lang()) # noqa E501
    else:
        raise Exception('Bad language for map styling, bro.')

    atlas = at(
        data_uri=get_resource_abspath('data/profile_data_structure_template.xlsx'),  # noqa: E501

        wards_uri=wards_uri or get_resource_abspath('mapfiles/hrrp_shapes/jsons/merge.json'),  # noqa: E501
        palika_uri=palika_uri or get_resource_abspath('mapfiles/hrrp_shapes/jsons/GaPaNaPa_hrrp.json'),  # noqa: E501
        dists_uri=dists_uri or get_resource_abspath('mapfiles/hrrp_shapes/jsons/Districts_hrrp.json'),  # noqa: E501

        dists_syle=dists_style_uri or get_resource_abspath('mapfiles/styles/dist_style.qml'),  # noqa: E501
        pka_style=pka_style_lang_uri or pka_style_lang,
        pka_hide_style=pka_hide_style_uri or get_resource_abspath('mapfiles/styles/palika_hide_style.qml'),  # noqa: E501
        ward_style=ward_style_uri or get_resource_abspath('mapfiles/styles/ward_style.qml'),  # noqa: E501
        atlas_style=atlas_style_uri or get_resource_abspath('mapfiles/styles/atlas_layout.qpt'),  # noqa: E501

        parent_join_cd='N_WCode',
        to_join_code='ward',
        pka_list=pka_list,
        img_type=img_type,

        out_path=get_resource_abspath('mapfiles/map_tmp/')
    )

    atlas.setup()
    atlas.make_maps()
    atlas.exit()
    del(atlas)


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
    except Exception:
        pass

    return False
