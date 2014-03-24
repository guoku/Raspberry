from django import forms
# from django.forms import widgets
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

class SignInAccountForm(forms.Form):
    error_messages = {
        'wrong_email': _("Your email is wrong."),
        'email_not_exist': _("email is not signed up."),
        'wrong_password': _("The password is wrong."),
    }

    next = forms.CharField(required=False, widget=forms.HiddenInput())
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('email')}),
                             label=_('email'), help_text=_(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('password')}),
                               label=_('password'), help_text=_(''), min_length=6, max_length=20)

    def clean_email(self):
        # log.info(self.cleaned_data )
        cleaned_data = self.cleaned_data
        # log.info(cleaned_data)
        data_email = cleaned_data['email']
        user_id = User.get_user_id_by_email(data_email)
        # is_exist = User.objects.filter(email=data_email).exists()
        if user_id is None:
            raise forms.ValidationError(
                self.error_messages['email_not_exist']
            )
        return user_id

    def clean(self):
        cleaned_data = super(SignInAccountForm, self).clean()
        log.info(cleaned_data)
        uid = cleaned_data.get('email', None)
        if not uid:
            raise forms.ValidationError(
                self.error_messages['wrong_email'],
            )
        password = cleaned_data.get('password', None)
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
    }
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('nickname')}),
                               label=_('nickname'), help_text=_(''))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('email')}),
                             label=_('email'), help_text=_(''))
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

class SignUpAccountBioFrom(forms.Form):
    avatar = forms.FileField(label=_('select a file'), help_text=_('max. 2 megabytes'), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows':'4', 'class':'textarea-input'}),
                          label=_('bio'), help_text=_(''), required = False)
    gender = forms.ChoiceField(widget = forms.RadioSelect(), choices = GENDER_CHOICES,
                               label = _('gender'), help_text = _(''), required = False)
    website = forms.URLField(widget=forms.TextInput(attrs={'class':'text-input'}),
                             label=_('website'), help_text=_(''), required = False)
    location = forms.CharField(widget=forms.Select(attrs={"name" : "location", "class" : "location"}),
                               label=_('location'),
                               required = False)
    city = forms.CharField(widget=forms.Select(attrs={'name' : 'city', 'class' : 'city'}),
                           label=_('city'),
                           required = False)

class SettingAccountForm(SignUpAccountBioFrom):
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class':'text-input'}),
                               label=_('nickname'), help_text=_(''), required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('email')}),
                             label=_('email'), help_text=_(''))

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('old password')}), label=_('old password'), help_text=_(''))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('new password')}), label=_('new password'), help_text=_(''), min_length=6, max_length=20)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('confirm password')}), label=_('confirm password'), help_text=_(''), min_length=6, max_length=20)

    def __init__(self, user, data=None):
        self.user = user
        super(ChangePasswordForm, self).__init__(data=data)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        old_password = cleaned_data.get('old_password')
        if self.user.check_password(old_password):
            if cleaned_data['new_password'] != cleaned_data['confirm_password']:
                raise forms.ValidationError("password mismatch")
        else:
            raise forms.ValidationError(
                "wrong password"
            )
        return cleaned_data
