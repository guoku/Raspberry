# -*- coding: utf-8 -*-
from django.db import models



class App_Pubilsh(models.Model):
    name = models.CharField(max_length = 150, blank = True)
    file = models.CharField(max_length = 255, blank = True)
    is_published = models.BooleanField(default = False)
    uploaded_time = models.DateTimeField(auto_now_add = True, editable = False)

    class Meta:
        ordering = ['-uploaded_time']

    def __unicode__(self):
        return self.name


    def get_url(self):
        return "/%s" % self.file

__author__ = 'edison'
