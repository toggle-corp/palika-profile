"""fot getting string vals for boilerplate values. also handles translation"""

title_strings = {}
header_strings = {}
lang = None


def set_lang(l):
    global lang
    assert l in ('en', 'np')
    lang = l


def get_lang():
    return lang


def import_titles(sht):
    """import titles from xls with en and np. give bad value if blank?"""
    global title_strings
    title_strings = {}

    for r in sht[['english', 'nepali']].iterrows():
        cd = r[0]
        en = r[1]['english']
        np = r[1]['nepali']

        # TODO: error?
        if cd in title_strings:
            raise Exception('Duplicate entry for %s in Titles xls' % cd)

        title_strings[cd] = {'en': en, 'np': np}


def import_data_header(cols):
    """import column names from header sheet"""
    global header_strings
    header_strings = cols


def boil(key):
    if key not in title_strings:
        # TODO: error
        print('Key not in xls: %s' % str(key))
        return ('***VALUE NOT IN XLS***')

    if title_strings[key][lang] is None:
        # TODO: error
        print('String value not in xls for language %s: %s' % (lang, str(key)))
        return('***VALUE NOT IN XLS***')

    return title_strings[key][lang]


def boil_header(key, override = False):
    """used for getting specific language version of a header in profile data. is different than boil()
        in that boil() works on the titles worksheet - this is used for specifying different language values
        for dynamic content in profiles"""
    NEPALI_POSTFIX = '_np'

    if lang == 'np':
        key += '_np'

    if key not in header_strings and not override:
        raise Exception('%s not in header_strings!' % key)

    return key