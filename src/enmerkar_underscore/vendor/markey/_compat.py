import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


_identity = lambda x: x


if not PY2:
    text_type = str
    string_types = (str,)
    integer_types = (int, )
    unichr = chr

    text_to_native = lambda s, enc: s

    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())

    from io import StringIO, BytesIO
    import pickle

    izip = zip
    imap = map
    range_type = range

    cmp = lambda a, b: (a > b) - (a < b)

else:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)

    text_to_native = lambda s, enc: s.encode(enc)
    unichr = unichr

    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()

    from cStringIO import StringIO as BytesIO
    from StringIO import StringIO
    import cPickle as pickle

    from itertools import izip, imap
    range_type = xrange

    cmp = cmp


number_types = integer_types + (float,)


# Mostly taken from Django.
def force_text(s, encoding='utf-8', errors='strict'):
    # Handle the common case first for performance reasons.
    if isinstance(s, text_type):
        return s
    try:
        if not isinstance(s, string_types):
            if PY3:
                if isinstance(s, bytes):
                    s = text_type(s, encoding, errors)
                else:
                    s = text_type(s)
            elif hasattr(s, '__unicode__'):
                s = text_type(s)
            else:
                s = text_type(bytes(s), encoding, errors)
        else:
            # Note: We use .decode() here, instead of six.text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise UnicodeDecodeError(s, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join([force_text(arg, encoding, errors) for arg in s])
    return s
