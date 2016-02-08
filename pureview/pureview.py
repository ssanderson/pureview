"""
pureview
--------
"""
from functools import wraps
from inspect import getfullargspec, Signature, Parameter
from weakref import WeakKeyDictionary


def make_init(slots):
    sig = Signature(
        [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in slots]
    )

    def init(self, *args, **kwargs):
        args = sig.bind(*args, **kwargs)
        for name, value in args.arguments.items():
            setattr(self, name, value)

    return init


class lazyval:
    """A memoizing property.

    Parameters
    ----------
    func : callable
        The function used to compute the value of the descriptor.
    """
    def __init__(self, func):
        self._cache = WeakKeyDictionary()
        self._func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self

        cache = self._cache
        try:
            return cache[instance]
        except KeyError:
            cache[instance] = val = self._func(instance)
            return val



def make_getter(spec, meth):

    @property
    @wraps(meth)
    def _meth(self):
        kwargs = {name: getattr(self, name) for name in spec.args}
        return meth(**kwargs)
    return _meth


class ViewMeta(type):

    def __new__(mcls, name, bases, clsdict):
        if '__slots__' not in clsdict:
            clsdict['__slots__'] = ()

        if '__init__' in clsdict:
            raise TypeError("Custom __init__'s not supported")

        clsdict['__init__'] = make_init(clsdict['__slots__'])

        for name, meth in clsdict.items():
            if name.startswith('__'):
                continue
            try:
                spec = getfullargspec(meth)
            except TypeError:
                continue
            clsdict[name] = make_getter(spec, meth)

        return super().__new__(mcls, name, bases, clsdict)


class View(metaclass=ViewMeta):
    pass
