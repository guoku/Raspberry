from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.log import getLogger

from base.handle_image import HandleImage
from base.models import Show_Event_Banner, Event_Banner

log = getLogger('django')

from django.conf import settings
image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')

class BaseBannerForm(forms.Form):

    link = forms.URLField(
        label=_('link'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )
    event_banner_image = forms.FileField(
        label=_('event banner image'),
        widget=forms.FileInput(attrs={'class':'controls'}),
        help_text=_(''),
    )

    def __init__(self, *args, **kwargs):
        super(BaseBannerForm, self).__init__(*args, **kwargs)
        (none, first, second, third, fourth, fifth) = (0, 1, 2, 3, 4, 5)
        BANNER_POSITION_CHOICES = (
            (none, _("none")),
            (first, _("first")),
            (second, _("second")),
            (third, _("third")),
            (fourth, _("fourth")),
            (fifth, _("fifth")),
        )
        self.fields['position'] = forms.ChoiceField(label=_('position'),
                                                  choices=BANNER_POSITION_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control',}),
                                                  help_text=_(''))

    def clean_position(self):
        _position = self.cleaned_data.get('position')
        return int(_position)

class CreateEventBannerForms(BaseBannerForm):
    #
    # link = forms.URLField(
    #     label=_('link'),
    #     widget=forms.TextInput(attrs={'class':'form-control'}),
    #     help_text=_(''),
    # )
    # event_banner_image = forms.FileField(
    #     label=_('event banner image'),
    #     widget=forms.FileInput(attrs={'class':'controls'}),
    #     help_text=_(''),
    # )

    def save(self):
        link = self.cleaned_data.get('link')
        event_banner_image = self.cleaned_data.get('event_banner_image')
        position = self.clean_position()
        # log.info(event_banner_image)
        _image = HandleImage(event_banner_image)
        file_path = "%s%s.jpg" % (image_path, _image.name)
        f = default_storage.save(file_path, ContentFile(_image.image_data))
        log.info(f)
        #
        _event_banner = Event_Banner.objects.create(
            link = link,
        )
        #
        # if position > 0:
        #     show = Show_Event_Banner.objects.get(pk = position)
        #     show.banner = _event_banner
        #     show.save()
        # pass

class EditEventBannerForms(BaseBannerForm):

    # link = forms.URLField(
    #     label=_('link'),
    #     widget=forms.TextInput(attrs={'class':'form-control'}),
    #     help_text=_(''),
    # )
    #
    # event_banner_image = forms.FileField(
    #     label=_('event banner image'),
    #     widget=forms.FileInput(attrs={'class':'controls'}),
    #     help_text=_(''),
    # )

    def __init__(self, banner, *args, **kwargs):
        self.banner = banner
        super(EditEventBannerForms, self).__init__(*args, **kwargs)
        if self.banner.has_show_banner:
            (none, first, second, third, fourth, fifth) = (0, 1, 2, 3, 4, 5)
            BANNER_POSITION_CHOICES = (
                # (none, _("none")),
                (first, _("first")),
                (second, _("second")),
                (third, _("third")),
                (fourth, _("fourth")),
                (fifth, _("fifth")),
            )
            self.fields['position'] = forms.ChoiceField(label=_('position'),
                                                  choices=BANNER_POSITION_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control',}),
                                                  help_text=_(''))

    def save(self):
        pass


__author__ = 'edison'
