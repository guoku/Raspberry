from django import forms
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# from django.contrib.auth import login as auth_login
from base.user import User

from django.utils.log import getLogger

log = getLogger('django')



class AccountFrom(forms.Form):
    error_messages = {
        'email_not_exist': _("email is not signed up."),
        # 'password_mismatch': _("The two password fields didn't match."),
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


class SignInAccountForm(AccountFrom):

    def signin(self):
        uid = self.cleaned_data['email']
        password = self.cleaned_data['password']
        username = User(uid).get_username()
        log.info("username %s" % password)

        _user = authenticate(username=username, password=password)
        return _user


class SignUpAccountFrom(forms.Form):
    error_messages = {
        'email_exist': _("email is signed up."),
        'nickname_exist': _("nickname is signed up.")
        # 'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('email')}),
                             label=_('email'), help_text=_(''))
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('nickname')}),
                               label=_('nickname'), help_text=_(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('password')}),
                               label=_('password'), help_text=_(''))

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

    def signup(self):
        _email = self.cleaned_data['email']
        _nickname = self.cleaned_data['nickname']
        _passwd = self.cleaned_data['password']
        _new_user = User.create(email=_email, password=_passwd)
        _new_user.set_profile(nickname=_nickname)
        _username = _new_user.get_username()
        _user =  authenticate(username=_username, password=_passwd)
        return _user

__author__ = 'edison7500'
