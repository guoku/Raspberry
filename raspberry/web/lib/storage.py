from django.core.files.storage import Storage

class FakeFileSystemStorage(Storage):
    def __init__(self, location=None, base_url=None):
        pass

    def open(self, name, mode='rb'):
        pass

    def save(self, name, content):
        pass

    def delete(self, name):
        pass

    def exists(self, name):
        pass

    def listdir(self, path):
        pass

    def size(self, name):
        pass

    def url(self, name):
        pass

    def accessed_time(self, name):
        pass

    def created_time(self, name):
        pass

    def modified_time(self, name):
        pass

__author__ = 'edison7500'
