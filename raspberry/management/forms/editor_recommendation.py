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
    editor_recommend_image = forms.FileField(
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

    def save(self):
        link = self.cleaned_data.get('link')
        editor_recommend_image = self.cleaned_data.get('editor_recommend_image')
        position = self.clean_position()
        # log.info(event_banner_image)
        _image = HandleImage(editor_recommend_image)
        file_path = "%s%s.jpg" % (image_path, _image.name)
        default_storage.save(file_path, ContentFile(_image.image_data))
        # log.info(f)
        #
        _recommendation = Editor_Recommendation.objects.create(
            link = link,
            image = file_path,
        )
        #
        if position > 0:
            try:
                show = Show_Editor_Recommendation.objects.get(pk = position)
                show.recommendation = _recommendation
                show.save()
            except Show_Editor_Recommendation.DoesNotExist:
                Show_Editor_Recommendation.objects.create(
                    recommendation =_recommendation
                )
        return _recommendation

class EditEditorRecommendForms(BaseRecommendationForm):

    def __init__(self, recommendation, *args, **kwargs):
        self.recommendation = recommendation
        super(EditEditorRecommendForms, self).__init__(*args, **kwargs)
        if self.recommendation.has_show_banner:
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
        editor_recommend_image = self.cleaned_data.get('editor_recommend_image')
        link = self.cleaned_data.get('link')
        position = self.clean_position()

        # log.info(position)
        self.recommendation.link = link

        if editor_recommend_image:
            _image = HandleImage(editor_recommend_image)
            file_path = "%s%s.jpg" % (image_path, _image.name)
            default_storage.save(file_path, ContentFile(_image.image_data))
            self.recommendation.image = file_path

        self.recommendation.save()

        if position > 0 and self.recommendation.position == 0:
            try:
                show = Show_Editor_Recommendation.objects.get(pk= position)
                show.recommendation = self.recommendation
                show.save()
            except Show_Editor_Recommendation.DoesNotExist:
                Show_Editor_Recommendation.objects.create(
                    recommendation = self.recommendation,
                )
        elif self.recommendation.position != position:
            show = Show_Editor_Recommendation.objects.get(pk = position)
            tmp_show = Show_Editor_Recommendation.objects.get(pk = self.recommendation.position)
            recommendation = show.recommendation
            show.recommendation = self.recommendation
            tmp_show.recommendation = recommendation

            show.save()
            tmp_show.save()



__author__ = 'edison'
