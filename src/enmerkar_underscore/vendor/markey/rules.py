import re
from ._compat import izip


def bygroups(*args):
    """
    Callback creator for bygroup yielding.
    """
    return lambda m: izip(args, m.groups())


class include(str):
    """
    Tells the lexer to include tokens from another set.
    """
    __slots__ = ()


class ruleset(tuple):
    __slots__ = ()

    def __new__(cls, *args):
        return tuple.__new__(cls, args)


class rule(object):
    """This represents a parsing rule."""
    __slots__ = ('match', 'token', 'enter', 'leave')

    def __init__(self, regexp, token=None, enter=None, leave=0):
        self.match = re.compile(regexp, re.U).match
        self.token = token
        self.enter = enter
        self.leave = leave
