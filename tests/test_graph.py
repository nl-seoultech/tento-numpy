from tento_num.graph import Space, DiffSpace


def test_sub_space():
    a = Space([1, 2])
    b = Space([2, 3, 4])
    r = b - a
    assert DiffSpace([1, 1.5]) == r
    assert r.average
    assert 1.25 == r.average
