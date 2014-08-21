from .graph import Space


def diff(g1, g2):
    s1 = Space(g1)
    s2 = Space(g2)
    return s1 - s2
