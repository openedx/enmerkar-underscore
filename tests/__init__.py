import pytest
from babel._compat import BytesIO

from enmerkar_underscore import extract

class TestMixedExtract:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.keywords = list(extract.DEFAULT_KEYWORDS.keys())

    def test_parses_django(self):
        buf = BytesIO(b'{% trans "Bunny" %}')
        messages = list(extract(buf, self.keywords, [], {}))
        assert messages == ([(1, None, 'Bunny', [])])

    def test_parses_blocktrans(self):
        buf = BytesIO(b'Ignored {% blocktrans %}{{ anton }}{% endblocktrans %}')
        messages = list(extract(buf, self.keywords, [], {}))
        assert messages == [(1, None, '%(anton)s', [])]

    def test_parses_underscore(self):
        buf = BytesIO(b'hello: <%= name %>')
        messages = list(extract(buf, self.keywords, [], {}))
        assert messages == []

    def test_parses_underscore_gettext(self):
        buf = BytesIO(b'hello: <%= gettext("name") %>')
        messages = list(extract(buf, self.keywords, [], {}))
        assert messages == [(1, 'gettext', 'name', [])]

    def test_extract_unicode(self):
        buf = BytesIO('<%= gettext("@ſðæ314“ſſ¶ÐĐÞ→SÆ^ĸŁ") %>'.encode())
        messages = list(extract(buf, self.keywords, [], {}))
        assert messages == [(1, 'gettext', '@ſðæ314“ſſ¶ÐĐÞ→SÆ^ĸŁ', [])]

    def test_extract_singular_form(self):
        buf = BytesIO(b'<%= _("foo") %> <%= _() %> <%= ngettext("foo", "bar", 42) %>')
        messages = list(extract(buf, self.keywords, [], {}))
        assert messages == [(1, '_', 'foo', []), (1, '_', (), []), (1, 'ngettext', ('foo', 'bar', None), [])]  # noqa

    def test_extract_singular_form_kwargs(self):
        buf = BytesIO(b'<%= _("foo") %> <%= _() %> <%= ngettext("foo", "bar", count=42) %>')
        messages = list(extract(buf, self.keywords, [], {}))
        assert messages == [(1, '_', 'foo', []), (1, '_', (), []), (1, 'ngettext', ('foo', 'bar', None, 'count'), [])]  # noqa#
