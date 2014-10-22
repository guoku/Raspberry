from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.log import getLogger

from base.handle_image import HandleImage
from base.models import Show_Editor_Recommendation, Editor_Recommendation

log = getLogger('django')

from django.conf import settings
image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')

class BaseRecommendationForm(forms.Form):

    link = forms.URLField(
        label=_('link'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )
    event_banner_image = forms.FileField(
        label=_('event banner image'),
        widget=forms.FileInput(attrs={'class':'controls'}),
        help_text=_(''),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(BaseRecommendationForm, self).__init__(*args, **kwargs)
        (none, first, second, third, fourth) = (0, 1, 2, 3, 4)
        BANNER_POSITION_CHOICES = (
            (none, _("none")),
            (first, _("first")),
            (second, _("second")),
            (third, _("third")),
            (fourth, _("fourth")),
        )
        self.fields['position'] = forms.ChoiceField(label=_('position'),
                                                  choices=BANNER_POSITION_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control',}),
                                                  help_text=_(''))

    def clean_position(self):
        _position = self.cleaned_data.get('position')
        return int(_position)

class CreateEditorRecommendForms(BaseRecommendationForm):
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
        default_storage.save(file_path, ContentFile(_image.image_data))
        # log.info(f)
        #
        _event_banner = Editor_Recommendation.objects.create(
            link = link,
            image = file_path,
        )
        #
        if position > 0:
            try:
                show = Show_Editor_Recommendation.objects.get(pk = position)
                show.banner = _event_banner
                show.save()
            except Show_Editor_Recommendation.DoesNotExist:
                Show_Editor_Recommendation.objects.create(
                    banner = _event_banner
                )
        return _event_banner

class EditEditorRecommendForms(BaseRecommendationForm):

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
        super(EditEditorRecommendForms, self).__init__(*args, **kwargs)
        if self.banner.has_show_banner:
            (none, first, second, third, fourth) = (0, 1, 2, 3, 4)
            BANNER_POSITION_CHOICES = (
                # (none, _("none")),
                (first, _("first")),
                (second, _("second")),
                (third, _("third")),
                (fourth, _("fourth")),
            )
            self.fields['position'] = forms.ChoiceField(label=_('position'),
                                                  choices=BANNER_POSITION_CHOICES,
                                                  widget=forms.Select(attrs={'class':'form-control',}),
                                                  help_text=_(''))

    def save(self):
        event_banner_image = self.cleaned_data.get('event_banner_image')
        position = self.clean_position()

        log.info(position)

        if event_banner_image:
            _image = HandleImage(event_banner_image)
            file_path = "%s%s.jpg" % (image_path, _image.name)
            default_storage.save(file_path, ContentFile(_image.image_data))
            self.banner.image = file_path
            self.banner.save()

        if position > 0 and self.banner.position == 0:
            show = Show_Editor_Recommendation.objects.get(pk= position)
            show.banner = self.banner
            show.save()
        elif self.banner.position != position:
            show = Show_Editor_Recommendation.objects.get(pk = position)
            tmp_show = Show_Editor_Recommendation.objects.get(pk = self.banner.position)
            tmp_banner = show.banner
            show.banner = self.banner
            tmp_show.banner = tmp_banner

            show.save()
            tmp_show.save()



__author__ = 'edison'
