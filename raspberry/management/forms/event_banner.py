from django import forms
from django.utils.translation import gettext_lazy as _

class BaseBannerForm(forms.Form):

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

    def save(self):

        pass

__author__ = 'edison'
