"""fot getting string vals for boilerplate values. also handles translation"""

strings = {}

def set_lang(l):
    global lang
    assert l in ('en', 'np')
    lang = l

def import_titles(sht):
    """import titles from xls with en and np. give bad value if blank?"""
    global strings
    MISSING_VAL = '**NO VALUE IN XLS**'
    strings = {}

    for r in sht[['english', 'nepali']].iterrows():
        cd = r[0]
        en = r[1]['english']
        np = r[1]['nepali']

        #TODO: error?
        if cd in strings:
            raise Exception('Duplicate entry for %s in Titles xls' % cd)

        strings[cd] = {'en' : en, 'np' : np}

def boil(key):
    if key not in strings:
        #TODO: error
        print('Key not in xls: %s' % str(key))
        print(strings)
        return ('***VALUE NOT IN XLS***')

    if strings[key][lang] is None:
        #TODO: error
        print('String value not in xls for language %s: %s' % (lang, str(key)))
        return('***VALUE NOT IN XLS***')

    return strings[key][lang]