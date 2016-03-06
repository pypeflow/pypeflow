# coding: utf-8
from datetime import datetime
import io
from pypeflow.plugins.base import BaseAsyncPlugin
from jinja2 import FileSystemLoader, Environment
import asyncio


class TemplateJinja2Plugin(BaseAsyncPlugin):

    name = 'Jinja2 Plugin'

    def __init__(self, filter_pattern='.html$', filter_collections=None, default_template='page.html',
                 env_kwargs=None):
        super().__init__(filter_pattern=filter_pattern, filter_collections=filter_collections)
        self.default_template = default_template
        self.templates_cache = {}
        self.env = None

        self.metadata = {}
        self.collections = {}
        self.env_kwargs = env_kwargs

    def pre_run(self, pypeflow, files):
        if 'loader' not in self.env_kwargs:
            self.env_kwargs['loader'] = FileSystemLoader(pypeflow.templates_path)
        self.env = Environment(**self.env_kwargs)
        self.metadata = pypeflow.metadata
        self.collections = pypeflow.collections

    def get_template(self, env, template_name):
        if not template_name:
            template_name = self.default_template

        return env.get_template(template_name)

    @asyncio.coroutine
    def process_file(self, path, file):
        template = self.get_template(self.env, file.get('template'))

        file['contents'].seek(0)
        file['contents'] = file['contents'].read().decode('utf-8')

        context = {
            'page': file,
            'metadata': self.metadata,
            'collections': self.collections,
            'strftime': datetime.now().strftime
        }

        file['contents'] = io.BytesIO(template.render(**context).encode('utf-8'))
