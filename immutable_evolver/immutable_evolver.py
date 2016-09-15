from abc import ABCMeta
import inspect
from collections import OrderedDict

from pyrsistent import pmap


def all_slots(cls):
    slot_names = OrderedDict()
    for base in inspect.getmro(cls):
        slot_names.update(
            (k, None) for k in getattr(base, '__slots__', ()))
    return tuple(slot_names)


class ImmutableEvolverMeta(ABCMeta):
    def __new__(metacls, name, bases, cls_dict):
        cls = super().__new__(metacls, name, bases, cls_dict)
        cls._all_slots = all_slots(cls)
        for base in bases:
            all_defaults = getattr(base, '_all_defaults', None)
            if all_defaults is not None:
                cls._all_defaults = all_defaults.update(dict(zip(
                    reversed(cls.__slots__), reversed(cls._defaults))))
                break
        return cls


class ImmutableEvolver(metaclass=ImmutableEvolverMeta):
    __slots__ = ()
    _defaults = ()
    _all_defaults = pmap()

    def __init__(self, *args, **kwargs):
        named_args = dict(zip(self._all_slots, args))
        kwargs = {'_' + k: v for k, v in kwargs.items()}
        assert not set(named_args) & set(kwargs)
        kwargs = self._all_defaults.update(named_args, kwargs)
        assert set(kwargs) == set(self._all_slots)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _evolve(self, **kwargs):
        members = ((k.lstrip('_'), getattr(self, k)) for k in self._all_slots)
        return type(self)(**dict(members, **kwargs))

    def __eq__(self, other):
        try:
            return self._all_slots == other._all_slots and all(
                getattr(self, k) == getattr(other, k) for k in self._all_slots)
        except AttributeError:
            return NotImplemented
