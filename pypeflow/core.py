# coding: utf-8
from __future__ import unicode_literals
from http.server import HTTPServer, CGIHTTPRequestHandler
from os import walk, chdir
from time import time
import io
import os
import re
import shutil


def get_collection_sort_function(collection_data):
    if 'sort' in collection_data:
        return lambda x: x.get(collection_data['sort'], 1)
    return lambda x: x['path']


class Pypeflow(object):

    def __init__(self, source_path=None, build_path=None, templates_path=None, plugins=None,
                 metadata=None, collections=None):
        assert source_path, 'source_path required'
        assert build_path, 'build_path required'
        assert templates_path, 'templates_path required'

        self.source_path = source_path.rstrip('/')
        self.build_path = build_path
        self.templates_path = templates_path
        self.plugins = plugins or {}
        self.metadata = metadata or {}
        self.collections = collections or {}
        self.files = {}

        self.read_files()

    def add_file(self, file):
        path = file['path']
        self.files[path] = file
        self.put_file_in_collections(path, file)

    def remove_file(self, path):
        removed_file = self.files.pop(path)

        for collection_name in removed_file['collections']:
            self.collections[collection_name]['files'].remove(removed_file)

        return removed_file

    def rename_file(self, path, new_path):
        if path != new_path:
            file = self.files.pop(path)
            file['path'] = new_path
            self.files[new_path] = file

    def update_file(self, path, file):
        old_file = self.files[path]
        old_file.update(file)

    def read_files(self):
        for (dirpath, dirnames, filenames) in walk(self.source_path):
            for filename in filenames:
                path, file = self.read_file('{}/{}'.format(dirpath, filename))
                self.add_file(file)

    def read_file(self, file_path):
        with io.open(file_path, 'rb') as f:
            contents = io.BytesIO(f.read())

        path = file_path[len(self.source_path):]
        file = {
            'path': path,
            'contents': contents,
            'collections': []
        }

        return path, file

    def write_files(self):
        for path, file in self.files.items():
            file_path = '{}{}'.format(self.build_path, path)

            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with io.open(file_path, 'wb') as f:
                f.write(file['contents'].read())

    def put_file_in_collections(self, source_path, file):
        for collection_name, collection_data in self.collections.items():
            if 'pattern' in collection_data and re.search(collection_data['pattern'], source_path):
                collection_files = collection_data.setdefault('files', [])
                collection_files.append(file)
                collection_data['files'] = sorted(collection_files, key=get_collection_sort_function(collection_data),
                                                  reverse=collection_data.get('reverse', False))
                file.setdefault('collections', []).append(collection_name)

    def clear_build_path(self):
        for the_file in os.listdir(self.build_path):
            file_path = os.path.join(self.build_path, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def build(self):
        started_at = time()
        print('Starting build process')

        self.clear_build_path()

        for plugin in self.plugins:
            plugin.run(self, self.files)

        self.write_files()

        print('Build finished in {:.5f}s'.format(time()-started_at))

    def serve(self, port=8000, host_name='localhost'):
        chdir(self.build_path)
        httpd = HTTPServer((host_name, port), CGIHTTPRequestHandler)
        print('Server started, open in your browser: http://{}:{} - to quit press <ctrl-c>'.format(host_name, port))
        httpd.serve_forever()
