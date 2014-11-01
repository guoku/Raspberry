from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.log import getLogger


from base.handle_image import HandleImage
from base.models import Banner

from django.conf import settings
image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')

log = getLogger('django')


class BaseBannerFrom(forms.Form):


    key = forms.CharField(
        label=_('key'),
        widget=forms.TextInput(attrs={'class':'input-xxlarge'}),
        help_text=_('key')
    )

    banner_image = forms.FileField(
        label=_('image'),
        widget=forms.FileInput(attrs={'type':'file'}),
        help_text=_(''),
    )

    weight = forms.IntegerField(
        label=_('weight'),
        widget=forms.TextInput(attrs={'type':'text', 'class':'input-xxlarge'}),
        help_text=_('')
    )

    def __init__(self, *args, **kwargs):
        super(BaseBannerFrom, self).__init__(*args, **kwargs)

        (entity, category, user, user_tag, outlink) = ('entity', 'category', 'user', 'user_tag', 'outlink')
        CONTENT_TYPE_CHOICES = (
            (entity, _("entity")),
            (category, _("category")),
            (user, _("user")),
            (user_tag, _("user_tag")),
            (outlink, _("outlink")),
        )
        self.fields['content_type'] = forms.ChoiceField(
            label=_('content_type'),
            choices=CONTENT_TYPE_CHOICES,
            widget=forms.Select(),
            help_text=_(""),
        )


class CreateBannerForm(BaseBannerFrom):

    def save(self):
        key = self.cleaned_data.get('key')
        weight = self.cleaned_data.get('weight')
        content_type = self.cleaned_data.get('content_type')
        banner_image = self.cleaned_data.get('banner_image')

        _image = HandleImage(banner_image)
        file_path = "%s%s.jpg" % (image_path, _image.name)
        default_storage.save(file_path, ContentFile(_image.image_data))

        banner = Banner.objects.create(
            key = key,
            weight = weight,
            content_type = content_type,
            image = file_path,
        )
        return banner
__author__ = 'edison'
