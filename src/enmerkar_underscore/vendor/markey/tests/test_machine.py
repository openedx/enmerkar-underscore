from enmerkar_underscore.vendor.markey.machine import tokenize, parse_arguments
from enmerkar_underscore.vendor.markey.tools import TokenStream
from enmerkar_underscore.vendor.markey.underscore import rules as underscore_rules


def test_parse_arguments():
    line = '<% gettext(varible, "some string", str="foo")'
    stream = TokenStream.from_tuple_iter(tokenize(line, underscore_rules))
    stream.next()
    stream.next()
    stream.expect('gettext_begin')
    stream.expect('func_name').value
    args, kwargs = parse_arguments(stream, 'gettext_end')
    assert args == (('varible', 'text'), ('some string', 'func_string_arg'),)
    assert kwargs == {'str': 'foo'}
