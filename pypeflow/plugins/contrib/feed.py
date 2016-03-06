# coding: utf-8
from datetime import datetime
import PyRSS2Gen
import io
from pypeflow.plugins.base import BasePlugin


class FeedPlugin(BasePlugin):

    name = 'Feed Plugin'

    def __init__(self, filter_pattern=None, filter_collections=None, path='/feed.xml'):
        super().__init__(filter_pattern=filter_pattern, filter_collections=filter_collections)
        self.path = path

    def process_files(self, pypeflow, files):
        rss = PyRSS2Gen.RSS2(
            title="Andrew's PyRSS2Gen feed",
            link="http://www.dalkescientific.com/Python/PyRSS2Gen.html",
            description=pypeflow.metadata.get('site', {}).get('description', ''),

            lastBuildDate=datetime.now(),

            items=[
                PyRSS2Gen.RSSItem(
                    title=file['title'],
                    link="{}{}".format(pypeflow.metadata.get('site', {}).get('url', ''), file['url']),
                    description=file.get('description'),
                    guid=PyRSS2Gen.Guid("{}{}".format(pypeflow.metadata.get('site', {}).get('url', ''), file['url'])),
                ) for file in files.values()])
        contents = io.BytesIO()
        rss.write_xml(contents)
        contents.seek(0)

        pypeflow.add_file({
            'path': self.path,
            'contents': contents,
            'collections': [],
        })

        return ()

    def process_file(self, path, file):
        pass
