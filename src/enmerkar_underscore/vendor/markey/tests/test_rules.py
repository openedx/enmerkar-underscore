import re

from markey.rules import bygroups, rule, ruleset


def test_bygroups():
    match = re.match(r'(1)(2)', '12')
    assert list(bygroups(('one',))(match)) == [(('one',), '1')]


class test_rule():
    r = rule(r'(\d)', 'num', 'do_number')
    assert r.match('1').group() == '1'
    assert r.token == 'num'
    assert r.enter == 'do_number'
    assert r.leave == 0


class test_ruleset():
    rs = ruleset(rule(r'(\d)', 'num', 'do_number'),)
    assert isinstance(rs, tuple)
