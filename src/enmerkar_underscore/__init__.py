import django
from django.template.base import Lexer

if django.VERSION[:2] >= (2, 1):
    from django.template.base import TokenType
    TOKEN_TEXT = TokenType.TEXT
else:  # django < 2.1
    from django.template.base import TOKEN_TEXT

from django.utils.encoding import force_str
from enmerkar.extract import extract_django

from .vendor.markey import underscore
from .vendor.markey.machine import parse_arguments, tokenize
from .vendor.markey.tools import TokenStream

__version__ = '2.4.0'

def extract(fileobj, keywords, comment_tags, options):
    """Extracts translation messages from underscore template files.

    This method does also extract django templates. If a template does not
    contain any django translation tags we always fallback to underscore extraction.

    This is a plugin to Babel, written according to
    http://babel.pocoo.org/docs/messages/#writing-extraction-methods

    :param fileobj: the file-like object the messages should be extracted
                    from
    :param keywords: a list of keywords (i.e. function names) that should
                     be recognized as translation functions
    :param comment_tags: a list of translator tags to search for and
                         include in the results
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)``
             tuples
    :rtype: ``iterator``
    """
    encoding = options.get('encoding', 'utf-8')

    original_position = fileobj.tell()

    text = fileobj.read().decode(encoding)

    if django.VERSION[:2] >= (1, 9):
        tokens = Lexer(text).tokenize()
    else:
        tokens = Lexer(text, None).tokenize()

    vars = [token.token_type != TOKEN_TEXT for token in tokens]

    could_be_django = any(list(vars))

    if could_be_django:
        fileobj.seek(original_position)
        iterator = extract_django(fileobj, keywords, comment_tags, options)
        for lineno, funcname, message, comments in iterator:
            yield lineno, funcname, message, comments
    else:
        # Underscore template extraction
        comments = []

        fileobj.seek(original_position)

        for lineno, line in enumerate(fileobj, 1):
            funcname = None

            stream = TokenStream.from_tuple_iter(tokenize(line, underscore.rules))
            while not stream.eof:
                if stream.current.type == 'gettext_begin':
                    stream.expect('gettext_begin')
                    funcname = stream.expect('func_name').value
                    args, kwargs = parse_arguments(stream, 'gettext_end')

                    strings = []

                    for arg, argtype in args:
                        if argtype == 'func_string_arg':
                            strings.append(force_str(arg))
                        else:
                            strings.append(None)

                    for arg in kwargs:
                        strings.append(None)

                    if len(strings) == 1:
                        strings = strings[0]
                    else:
                        strings = tuple(strings)

                    yield lineno, funcname, strings, []

                stream.next()
