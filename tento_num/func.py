from math import ceil
from itertools import groupby

from numpy import polyfit, linspace

from .graph import Space


def diff(g1, g2):
    s1 = Space(g1)
    s2 = Space(g2)
    dif = s1 - s2
    return dif.average


def poly_reg(y, deg=2):
    x = linspace(0, 1, len(y))
    return polyfit(x, y, deg=deg)


def remove_zero(s):
    for x in s:
        if x != 0:
            yield x


def remove_lower(s, percent=5):
    s = list(remove_zero(s))
    num_to_remove = ceil(len(s) * percent / 100)
    histo = [(x[0], len(list(x[1]))) for x in groupby(sorted(s))]
    histo = sorted(histo, key=lambda x: x[0])
    h = histo[:num_to_remove]
    i = 0
    filter_ = {}
    while num_to_remove > 0:
        num_to_remove -= histo[i][1]
        if num_to_remove > histo[i][1]:
            sub = histo[i][1]
        else:
            sub = num_to_remove
        filter_[histo[i][0]] = sub
        i += 1
    filter_keys = filter_.keys()
    r = []
    for x in s:
        if x in filter_keys and filter_[x] > 0:
            filter_[x] -= 1
        else:
            r.append(x)
    return r
