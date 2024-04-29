from .rules import include
from ._compat import force_text


def iter_rules(x, rules):
    for rule in rules[x]:
        if rule.__class__ is include:
            for item in iter_rules(rule, rules):
                yield item
        else:
            yield rule


def tokenize(string, rules, encoding='utf-8'):
    string = force_text(string)

    pos = 0
    end = len(string)
    stack = [(None, 'everything')]
    rule_cache = {}
    text_buffer = []
    add_text = text_buffer.append
    push = stack.append
    flatten = ''.join

    while pos < end:
        state = stack[-1][1]
        if state not in rule_cache:
            rule_cache[state] = list(iter_rules(state, rules))
        for rule in rule_cache[state]:
            m = rule.match(string, pos)
            if m is not None:
                # first flush text that is left in the buffer
                if text_buffer:
                    text = flatten(text_buffer)
                    if text:
                        yield 'text', text
                    del text_buffer[:]

                # now enter the new scopes if entered in a
                # non silent way
                if rule.enter is not None:
                    push((rule.enter + '_end', rule.enter))
                    yield rule.enter + '_begin', m.group()

                # now process the data
                if callable(rule.token):
                    for item in rule.token(m):
                        yield item
                elif rule.token is not None:
                    yield rule.token, m.group()

                # now check if we leave something. if the state was
                # entered non silent, send a close token.
                pos = m.end()
                for x in range(rule.leave):
                    announce, item = stack.pop()
                    if announce is not None:
                        yield announce, m.group()

                break
        else:
            char = string[pos]
            add_text(char)
            pos += 1

    # if the text buffer is left filled, we flush it
    if text_buffer:
        text = flatten(text_buffer)
        if text:
            yield 'text', text

    # if there are things in the stack left we should
    # emit the end tokens
    for announce, item in reversed(stack):
        if announce is not None:
            yield announce, u''


def parse_arguments(stream, end_token):
    """
    Helper function for function argument parsing.  Pass it a
    `TokenStream` and the delimiter token for the argument section and
    it will extract all position and keyword arguments as well as
    each argument's type info (string literal or not).

    Returns a ``(args, kwargs)`` tuple.
    """
    args = []
    kwargs = {}
    keywords = []
    while stream.current.type != end_token:
        if stream.current.type == 'func_string_arg':
            value = stream.current.value.strip()
            for char in ['\'', '"']:
                if value.startswith(char) and value.endswith(char):
                    value = value[1: -1]
                    break
            stream.next()
            if keywords:
                for keyword in keywords:
                    kwargs[keyword] = value
                del keywords[:]
            else:
                args.append((value, 'func_string_arg'))
        elif stream.current.type == 'text':
            args.append((stream.current.value, 'text'))
            stream.next()
        elif stream.current.type == 'func_kwarg':
            keywords.append(stream.current.value)
            stream.next()
        elif stream.current.type == 'func_argument_delimiter':
            stream.next()
        else:
            break
    for keyword in keywords:
        args.append((keyword, 'func_kwarg'))

    return tuple(args), kwargs
