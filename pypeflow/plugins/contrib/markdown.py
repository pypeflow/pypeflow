# coding: utf-8
from pypeflow.plugins.base import BaseThreadPlugin
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from html import escape
import os
import io
import misaka


class HighlighterRenderer(misaka.HtmlRenderer):
    def blockcode(self, text, lang):
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(escape(text.strip()))

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()

        return highlight(text, lexer, formatter)


class MarkdownPlugin(BaseThreadPlugin):

    name = 'Markdown Plugin'

    def __init__(self, filter_pattern=r'\.m(d|arkdown)$', filter_collections=None, highlight_options=None,
                 markdown_extensions=()):
        super().__init__(filter_pattern=filter_pattern, filter_collections=filter_collections)
        self.highlight_options = highlight_options or {}

        renderer = HighlighterRenderer(**self.highlight_options)
        self.markdown = misaka.Markdown(renderer=renderer, extensions=markdown_extensions)

    def process_file(self, path, file):
        file['contents'].seek(0)
        contents = self.markdown(file['contents'].read().decode(encoding='UTF-8'))
        file['contents'] = io.BytesIO(bytes(contents, 'UTF-8'))

        filename, _ = os.path.splitext(path)

        return (
            ('rename_file', {'old_path': path, 'new_path': '{}.html'.format(filename)}),
        )
