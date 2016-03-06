# coding: utf-8
import io
from pypeflow.plugins.base import BaseThreadPlugin
from frontmatter import parse


class FrontmatterPlugin(BaseThreadPlugin):
    name = 'Frontmatter Plugin'

    def process_file(self, path, file):
        metadata, contents = parse(file['contents'].read())

        if metadata.pop('path', None) or metadata.pop('collections', None):
            self.log_error('{}: path and collections are reserved keywords'.format(path))

        file.update(metadata)
        file['contents'] = io.BytesIO(bytes(contents, 'UTF-8'))
