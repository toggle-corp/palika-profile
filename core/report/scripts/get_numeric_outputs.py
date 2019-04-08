"""module for testing what output of numeric types will look like"""
import sys

sys.path.extend(['.', '..'])
from common import boiler, utils

def p(inp, out):
    print(inp + ' >> ' + out)

for i in range(2):
    print()
    print(boiler.get_lang())
    print()

    print('Num')
    print()
    p('1 ' , utils.fmt_num(1))
    p('1000 ' , utils.fmt_num(1000))
    p('1000000 ' , utils.fmt_num(1000000))
    p('.55' , utils.fmt_num(int(.55)))
    p('5.5' , utils.fmt_num(int(5.5)))

    print()
    print('Dec')
    print()
    p('0' , utils.fmt_dec(0, 2))
    p('.4' , utils.fmt_dec(.4, 2))
    p('5.5' , utils.fmt_dec(5.5, 2))
    p('6' , utils.fmt_dec(6, 2))
    p('6444.23', utils.fmt_dec(6444.23, 2))
    p('6.889', utils.fmt_dec(6.889, 2))

    print()
    print('Pct')
    print()

    p('0' , utils.fmt_pct(0, 2))
    p('.344455' , utils.fmt_pct(.344455, 2))
    p('.3' , utils.fmt_pct(.3, 2))
    p('1' , utils.fmt_pct(1, 2))
    p('1.3' , utils.fmt_pct(1.3, 2))

    boiler.set_lang('np')