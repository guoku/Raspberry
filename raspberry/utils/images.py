from wand.image import Image as WandImage
from hashlib import md5


class HandleImage(object):

    def __init__(self, image_file):
        if hasattr(image_file, 'chunks'):
            self._image_data = ''.join(chunk for chunk in image_file.chunks())
        else:
            self._image_data = image_file.read()
        image_file.close()
        self._name = None

    @property
    def image_data(self):
        return self._image_data

    @property
    def name(self):
        self._name = md5(self.image_data).hexdigest()
        return self._name

    def resize(self, w, h):
        _img = WandImage(blob = self.image_data)

        if (w / h > _img.width / _img.height):
            _width = round(h * _img.width / _img.height)
            _height = h
        else:
            _width = w
            _height = round(w * _img.height / _img.width)
        _width = int(_width)
        _height = int(_height)
        _img.resize(_width, _height)
        return _img.make_blob()



__author__ = 'edison7500'
