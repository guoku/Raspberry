from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# from django.contrib.auth import login as auth_login
from base.user import User

from django.utils.log import getLogger

log = getLogger('django')


Man = u'M'
Woman = u'F'
Other = u'O'
GENDER_CHOICES = (
        (Man, _('male')),
        (Woman,  _('female')),
        (Other,  _('other')),
    )

class LocationSelectWidget(widgets.MultiWidget):
    def __init__(self, attrs = None):
        # years = [(year, year) for year in (2011, 2012, 2013)]
        _widgets = (
            widgets.Select(attrs=attrs, choices=[]),
            widgets.Select(attrs=attrs, choices=[]),
        )

        super(LocationSelectWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value]
        return [None]


class LocationSelectField(forms.MultiValueField):
    widget = LocationSelectWidget
    default_error_messages = {
            'invalid_location':_(''),
            'invalid_city':_(''),
    }

    def __init__(self, *args, **kwargs):
        localize = kwargs.get('localize', False)
        fields = (
            widgets.Select(choices=[], localize=localize),
        )
        super(LocationSelectField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return data_list
        return None


class SignInAccountForm(forms.Form):
    error_messages = {
        'email_not_exist': _("email is not signed up."),
        'wrong_password': _("The password is wrong."),
    }

    next = forms.CharField(required=False, widget=forms.HiddenInput())
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('email')}),
                             label=_('email'), help_text=_(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('password')}),
                               label=_('password'), help_text=_(''))

    def clean_email(self):
        cleaned_data = self.cleaned_data
        data_email = cleaned_data['email']
        user_id = User.get_user_id_by_email(data_email)
        # is_exist = User.objects.filter(email=data_email).exists()
        if not user_id:
            raise forms.ValidationError(
                self.error_messages['email_not_exist']
            )
        return user_id

    def clean(self):
        cleaned_data = super(SignInAccountForm, self).clean()
        uid = cleaned_data['email']
        password = cleaned_data['password']
        username = User(uid).get_username()
        _user = authenticate(username = username, password = password)
        if not _user:
            raise forms.ValidationError(
                self.error_messages['wrong_password']
            )
        cleaned_data['user'] = _user
        return cleaned_data

class SignUpAccountFrom(forms.Form):
    error_messages = {
        'email_exist': _("email is signed up."),
        'nickname_exist': _("nickname is signed up."),
        'not_agree_tos': _("you must agree terms of service.")
        # 'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('email')}),
                             label=_('email'), help_text=_(''))
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('nickname')}),
                               label=_('nickname'), help_text=_(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('password')}),
                               label=_('password'), help_text=_(''))

    agree_tos = forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked' : 'checked'}))

    def clean_email(self):
        cleaned_data = self.cleaned_data
        data_email = cleaned_data['email']
        is_exist = User.email_exist(data_email)
        if is_exist:
            raise forms.ValidationError(
                self.error_messages['email_exist'],
            )
        return data_email

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        is_exist = User.nickname_exist(nickname)
        if is_exist:
            raise forms.ValidationError(
                self.error_messages['nickname_exist'],
            )
        return nickname

    def clean_agree_tos(self):
        if not self.cleaned_data['agree_tos']:
            raise forms.ValidationError(
                self.error_messages['not_agree_tos'],
            )
        return self.cleaned_data['agree_tos']
#
#    def signup(self):
#        _email = self.cleaned_data['email']
#        _nickname = self.cleaned_data['nickname']
#        _passwd = self.cleaned_data['password']
#        _new_user = User.create(email=_email, password=_passwd)
#        _new_user.set_profile(nickname=_nickname)
#        _username = _new_user.get_username()
#        _user =  authenticate(username=_username, password=_passwd)
#        return _user
#

class SignUpAccountBioFrom(forms.Form):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows':'4', 'class':'text-input'}),
                          label=_('bio'), help_text=_(''), required = False)
    gender = forms.ChoiceField(widget = forms.RadioSelect(), choices = GENDER_CHOICES,
                               label = _('gender'), help_text = _(''), required = False)
    website = forms.URLField(widget=forms.TextInput(attrs={'class':'text-input'}),
                             label=_('website'), help_text=_(''), required = False)
    location = forms.CharField(widget=forms.Select(attrs={"name" : "location", "class" : "location"}), required = False)
    city = forms.CharField(widget=forms.Select(attrs={'name' : 'city', 'class' : 'city'}), required = False)

class SettingAccountForm(forms.Form):
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class':'text-input'}),
                               label=_('nickname'), help_text=_(''))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'text-input'}),
                             label=_('email'), help_text=_(''))
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows':'4', 'class':'text-input'}),
                          label=_('bio'), help_text=_(''))
    # location = forms.MultiValueField(widget=LocationSelectWidget(attrs={'class':'location'}),
                                         # label=_('location'), help_text=_(""))
    gender = forms.ChoiceField(widget=forms.RadioSelect(), choices = GENDER_CHOICES, label = _('gender'), help_text = _(''))
    website = forms.URLField(widget=forms.TextInput(attrs={'class':'text-input'}),
                             label=_('website'), help_text=_(''))

__author__ = 'edison7500'
