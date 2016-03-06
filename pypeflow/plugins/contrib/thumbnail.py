# coding: utf-8
import os
from pypeflow.plugins.base import BaseThreadPlugin
from PIL import Image
import io


class ThumbnailPlugin(BaseThreadPlugin):

    name = 'Thumbnail Plugin'

    def __init__(self, filter_pattern=None, filter_collections=None, sizes=None):
        super().__init__(filter_pattern=filter_pattern, filter_collections=filter_collections)

        self.sizes = sizes or []

    def process_file(self, path, file):

        image = file['contents']

        thumbs_created = [self.create_thumb(path, image, size) for size in self.sizes]

        return [('add_file', {'file': thumb}) for thumb in thumbs_created]

    def create_thumb(self, path, image, size):
        filename, ext = os.path.splitext(path)
        thumb = io.BytesIO()
        thumb_path = '{}_thumb_{}x{}{}'.format(filename, size[0], size[1], ext)
        img = Image.open(image).copy()
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(thumb, format=Image.EXTENSION.get(ext, None))

        image.seek(0)
        thumb.seek(0)

        return {
            'path': thumb_path,
            'contents': thumb,
            'collections': []
        }
