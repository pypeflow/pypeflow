# coding: utf-8
import os
import io
import asyncio
import asyncio.subprocess
from pypeflow.plugins.base import BaseAsyncPlugin
from shlex import quote


class LessPlugin(BaseAsyncPlugin):

    name = 'Less Plugin'
    description = ''

    def __init__(self, filter_pattern=r'\.less', filter_collections=None, compress=True):
        super().__init__(filter_pattern=filter_pattern, filter_collections=filter_collections)
        self.compress = compress
        self.source_path = None

    @asyncio.coroutine
    def process_file(self, path, file):
        source_path = quote('{}{}'.format(self.source_path, path))
        proc = yield from asyncio.create_subprocess_shell(
            'lessc -s{} {}'.format(' -x' if self.compress else '', source_path),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        contents, err = yield from proc.communicate()

        if err:
            raise Exception('Error in less processing:\n{}\n{}'.format(path, err.decode('utf-8')))

        file['contents'] = io.BytesIO(contents)

    def pre_run(self, pypeflow, files):
        self.source_path = pypeflow.source_path

    def post_run(self, pypeflow, files):
        for path, file in files.items():
            filename, _ = os.path.splitext(path)
            pypeflow.rename_file(path, '{}.css'.format(filename))
