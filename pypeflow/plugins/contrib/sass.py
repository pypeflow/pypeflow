# coding: utf-8
import os
import asyncio
import io
from pypeflow.plugins.base import BaseThreadPlugin
from shlex import quote
import sass


class SassPlugin(BaseThreadPlugin):

    name = 'Sass Plugin'
    description = ''

    def __init__(self, filter_pattern=r'\.s[ac]ss$', filter_collections=None, compress=True):
        super().__init__(filter_pattern=filter_pattern, filter_collections=filter_collections)
        self.compress = compress
        self.source_path = None

    @asyncio.coroutine
    def process_file(self, path, file):
        source_path = quote('{}{}'.format(self.source_path, path))

        file['contents'] = io.BytesIO(sass.compile(filename=source_path, output_style='expanded').encode('utf-8'))

    def pre_run(self, pypeflow, files):
        self.source_path = pypeflow.source_path

    def post_run(self, pypeflow, files):
        for path, file in files.items():
            filename, _ = os.path.splitext(path)
            pypeflow.rename_file(path, '{}.css'.format(filename))
