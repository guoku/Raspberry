from django import forms
from django.utils.translation import gettext_lazy as _
from base.models import Event


class BaseEventForm(forms.Form):
    YES_OR_NO = (
        (True, _('yes')),
        (False, _('no')),
    )

    tag = forms.CharField(
        label=_('tag'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('')
    )

    slug = forms.CharField(
        label=_('slug'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )

    status = forms.ChoiceField(
        label=_('status'),
        choices=YES_OR_NO,
        widget=forms.Select( attrs={'class':'form-control'}),
        required=False,
        help_text=_(''),
    )


class CreateEventForm(BaseEventForm):


    def save(self):
        _tag = self.cleaned_data.get('tag')
        _slug = self.cleaned_data.get('slug')
        _status = self.cleaned_data.get('status')

        event = Event.objects.create(
            tag = _tag,
            slug = _slug,
            status = _status,
        )

        return event

__author__ = 'edison'
