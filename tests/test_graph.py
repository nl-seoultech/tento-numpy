from tento_num.graph import Space, DiffSpace

def test_space_get():
    l = Space([1,2,3])
    assert 1 == l.get(0)
    assert 2 == l.get(0.5)
    assert 3 == l.get(1)
    assert 2.2 == l.get(0.6)


def test_sub_space():
    a = Space([1, 2, 3])
    b = Space([2, 3, 4])
    r = b - a
    assert DiffSpace([1, 1, 1]) == r
    assert r.average
    assert 1 == r.average
    a = Space([1, 2, 3, 4])
    b = Space([2, 3, 4])
    r = b - a
    assert DiffSpace([1, 0.5, 0]) == r
    assert 0.5 == r.average
