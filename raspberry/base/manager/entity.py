from django.db import models
from django.db.models.query import QuerySet

class EntityQuerySet(QuerySet):
    def freeze(self):
        return self.filter(weight__lt=-1)

    def active(self):
        return self.filter()


class EntityManager(models.Manager):

    def get_query_set(self):
        return EntityQuerySet(self.model, self._db)

    def freeze(self):
        return self.get_query_set().freeze()

    def _create(self):
        pass

__author__ = 'edison7500'
