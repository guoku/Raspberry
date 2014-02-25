# -*- coding: utf-8 -*-
from django.db import models

class Email_List(models.Model):
    email = models.CharField(max_length = 64, db_index = True, unique = True)
    done = models.BooleanField(default = False)
