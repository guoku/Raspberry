from django.db import models

from django.conf import settings

APP_UPLOAD_DIR = getattr(settings, 'APP_UPLOAD_DIR', 'uploads/app/')

class App_Pubilsh(models.Model):
    name = models.CharField()
    file = models.FileField(upload_to=APP_UPLOAD_DIR)
    is_published = models.BooleanField(default=False)
    uploaded_time = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-uploaded_time']

    def __unicode__(self):
        return self.name

__author__ = 'edison'
