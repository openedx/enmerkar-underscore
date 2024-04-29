import sys
from six import StringIO

import pytest

from markey.tools import Token, TokenStream, TokenStreamIterator


def test_tokenstream():
    s = TokenStream(iter((Token('a', 1), Token('b', 2), Token('c', 3))))
    assert s.current == Token('a', 1)


def test_tokenstream_from_tuple_iter():
    # from_tuple_iter
    s = TokenStream.from_tuple_iter(iter((('a', 1), ('b', 2), ('c', 3))))
    assert s.current == Token('a', 1)

    # iter
    assert isinstance(iter(s), TokenStreamIterator)
    assert tuple(iter(s)) == (Token('a', 1), Token('b', 2), Token('c', 3))


def test_tokenstream_eof():
    # eof
    s = TokenStream(iter((Token('a', 1), Token('b', 2), Token('c', 3))))
    assert not s.eof
    list(s)
    assert s.eof


def test_tokenstream_look_push():
    # look, push
    s = TokenStream(iter((Token('a', 1), Token('b', 2), Token('c', 3))))
    assert s.current == Token('a', 1)
    assert s.look() == Token('b', 2)
    s.next()
    assert s.look() == Token('c', 3)
    s.push(Token('b', 2))
    assert s.look() == Token('b', 2)
    s.push(Token('e', 4), current=True)
    assert s.current == Token('e', 4)
    assert s.look() == Token('b', 2)


def test_tokenstream_skip_next():
    # skip, next
    s = TokenStream(iter((Token('a', 1), Token('b', 2), Token('c', 3))))
    s.skip(1)
    assert s.current == Token('b', 2)
    s.next()
    assert s.current == Token('c', 3)
    s.push(Token('e', 4))
    assert s.current == Token('c', 3)
    s.next()
    assert s.current == Token('e', 4)
    s.next()
    assert s.current == Token('eof', None)


def test_tokenstream_expect():
    # expect
    s = TokenStream(iter((Token('a', 1), Token('b', 2), Token('c', 3))))
    assert s.expect('a') == Token('a', 1)
    assert s.expect('b', 2) == Token('b', 2)
    pytest.raises(AssertionError, s.expect, 'e')
    pytest.raises(AssertionError, s.expect, 'c', 5)


def test_tokenstream_test_shift():
    # test
    s = TokenStream(iter((Token('a', 1), Token('b', 2), Token('c', 3))))
    assert s.test('a')
    s.next()
    assert s.test('b', 2)

    # shift
    assert s.current == Token('b', 2)
    s.shift(Token('f', 5))
    assert s.current == Token('f', 5)
    s.next()
    assert s.current == Token('b', 2)


def test_tokenstream_debug():
    stream = StringIO()

    _original_stdout = sys.stdout
    sys.stdout = stream

    try:
        s = TokenStream(iter((Token('a', 1),)))
        s.debug()
        assert stream.getvalue() == "Token(type='a', value=1)\n"
    finally:
        sys.stdout = _original_stdout
