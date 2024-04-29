# Full functioning underscore template parser.

from .rules import ruleset, include, rule, bygroups


keywords = frozenset((
    'pluralidx', 'gettext', 'ngettext', 'gettext_noop', 'pgettext',
    'npgettext', '_'
))


rules = {
    'everything': ruleset(
        include('inline'),
        include('function'),
    ),
    'inline': ruleset(
        rule(r'<%=', enter='interpolate'),
        rule(r'<%-', enter='escape'),
        rule(r'<%', enter='evaluate'),
    ),
    'inline_with_func': ruleset(
        include('inline'),
        include('function')
    ),
    'function': ruleset(
        rule(r'({keywords})\('.format(keywords='|'.join(keywords)),
             bygroups('func_name'), enter='gettext')
    ),
    'gettext': ruleset(
        rule(r'([\"\'])?\)', leave=1),
        include('function_call')
    ),
    'evaluate': ruleset(
        rule(r'%>', leave=1),
        include('inline_with_func'),
    ),
    'interpolate': ruleset(
        rule(r'%>', leave=1),
        include('inline_with_func'),
    ),
    'escape': ruleset(
        rule(r'%>', leave=1),
        include('inline_with_func'),
    ),
    # function calls (parse string arguments and implicit strings)
    'function_call': ruleset(
        rule(',', 'func_argument_delimiter'),
        rule('\s+', None),
        rule(r"(?s)('([^'\\]*(?:\\.[^'\\]*)*)'|"
             r'"([^"\\]*(?:\\.[^"\\]*)*)")', 'func_string_arg'),
        rule(r'([\w_]+)\s*=', bygroups('func_kwarg'))
    )
}
