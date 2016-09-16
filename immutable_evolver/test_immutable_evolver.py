from pytest import raises

from pyrsistent import pmap

from .immutable_evolver import ImmutableEvolver


class Foo(ImmutableEvolver):
    __slots__ = '_a', '_b'
    _defaults = 2,


class Bar(Foo):
    __slots__ = '_c', '_d'
    _defaults = 4,
    _eq_excl = '_d',


def test_slots_accumulate():
    assert Foo._all_slots == ('_a', '_b')
    assert Bar._all_slots == ('_c', '_d', '_a', '_b')


def test_defaults_correctly_attributed():
    assert Foo._all_defaults == pmap({'_b': 2})
    assert Bar._all_defaults == pmap({'_b': 2, '_d': 4})


def test_arg_order():
    bar = Bar(1, 2, 3, 4)
    assert bar._a == 3
    assert bar._b == 4
    assert bar._c == 1
    assert bar._d == 2


def test_mandatory_kwargs():
    bar = Bar(c=1, a=2)
    assert bar._a == 2
    assert bar._b == 2
    assert bar._c == 1
    assert bar._d == 4


def test_args_kwargs():
    bar = Bar(1, a=2)
    assert bar._a == 2
    assert bar._b == 2
    assert bar._c == 1
    assert bar._d == 4

    bar2 = bar._evolve(c=6)
    assert bar2 is not bar
    assert bar._c == 1
    assert bar2._c == 6
    assert bar2._a == bar._a
    assert bar2._b == bar._b
    assert bar2._d == bar._d


def test_assertion():
    raises(AssertionError, Bar)
    raises(AssertionError, Bar, 1, c=2)


def test_eq():
    assert Foo(1, 2) == Foo(1, 2)


def test_not_eq():
    assert Foo(1, 2) != Foo(3, 4)


def test_disparate_not_eq():
    assert Foo(a=1, b=2) != Bar(a=1, b=2, c=3, d=4)


def test_eq_excl():
    b = Bar(a=1, b=2, c=3, d=4)
    assert b == b._evolve(d=5)


def test_repr():
    f = Foo(1, 2)
    assert eval(repr(f)) == f
