from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# from django.contrib.auth import login as auth_login
from base.user import User

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
        return cleaned_data


class SignInAccountForm(AccountFrom):

    def signin(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        # next = self.cleaned_data['next']
        uid = User.get_user_id_by_email(email)
        username = User(uid).get_username()
        # _user = User.objects.get(email = email)

        _user = authenticate(username=username, password=password)
        return _user
        # if self.next:
        #     return self.next
        # else:


class SignUpAccountFrom(AccountFrom):
    nickname = forms.CharField(widget=forms.TextInput(), label=_('nickname'), help_text=_(''))

__author__ = 'edison7500'
