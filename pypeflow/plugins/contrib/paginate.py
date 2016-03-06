# coding: utf-8
import re
import io
from pypeflow.plugins.base import BasePlugin


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


class PaginatePlugin(BasePlugin):

    name = 'Paginate Plugin'

    def __init__(self, filter_pattern=None, filter_collections=None, per_page=10, template=None,
                 permalink_first=None, permalink=None, page_metadata=None, sort=None, sort_reverse=False):
        super().__init__(filter_pattern=filter_pattern, filter_collections=filter_collections)

        self.per_page = per_page
        self.template = template
        self.permalink_first = permalink_first
        self.permalink = permalink
        self.page_metadata = page_metadata
        self.sort = sort
        self.sort_reverse = sort_reverse

    def process_files(self, pypeflow, files):
        sorted_files = sorted(files.values(), key=lambda x: x[self.sort] if self.sort else x['path'],
                              reverse=self.sort_reverse)
        previous_page = None
        pages = chunks(sorted_files, self.per_page)

        for page_number, files_chunk in enumerate(pages, start=1):
            if page_number == 1 and self.permalink_first:
                url = re.sub(r':page', str(page_number), self.permalink_first)
            else:
                url = re.sub(r':page', str(page_number), self.permalink)

            url = '/{}/'.format(url.strip('/')).replace('//', '/')

            page = {
                'path': '{}index.html'.format(url),
                'contents': io.BytesIO(),
                'template': self.template,
                'collections': [],
                'url': url,
                'metadata': self.page_metadata,
                'paginator': {
                    'page_number': page_number,
                    'previous': previous_page,
                    'next': None,
                    'files': files_chunk,
                }
            }

            if previous_page:
                previous_page['paginator']['next'] = page

            previous_page = page

            pypeflow.add_file(page)

        return ()

    def process_file(self, path, file):
        pass
