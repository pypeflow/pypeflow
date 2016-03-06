# coding: utf-8
from __future__ import unicode_literals
import re
from pypeflow.plugins.base import BaseThreadPlugin
from slugify import slugify


class PermalinksPlugin(BaseThreadPlugin):

    name = 'Permalinks Plugin'
    description = """
    Generates a url attribute for each HTML file and rename the file to match the url
    if url is already set manually in frontmatter or by another plugin, just rename the file
    """

    def __init__(self, filter_pattern=r'\.html$', filter_collections=None):
        super().__init__(filter_pattern=filter_pattern, filter_collections=filter_collections)
        self.collections_permalinks = {}

    def process_file(self, path, file):

        url = file.get('url')
        if not url:
            permalink = self.get_permalink_pattern(file)
            url = '/{}/'.format(re.sub(r':(\w+)', lambda x: slugify(file[x.group(1)]), permalink)).replace('//', '/')
            file['url'] = url

        if url.endswith('/'):
            return (
                ('rename_file', {'old_path': path, 'new_path': '{}index.html'.format(url)}),
            )

    def pre_run(self, pypeflow, files):
        for collection_name, collection_data in pypeflow.collections.items():
            self.collections_permalinks[collection_name] = collection_data.get('permalink', ':title').strip('/')

    def get_permalink_pattern(self, file):
        if file['collections']:
            for collection in file['collections']:
                if collection in self.collections_permalinks:
                    return self.collections_permalinks[collection]
        return ':title'
