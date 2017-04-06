from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        if self.data['password'] != self.data['confirm_password']:
            raise forms.ValidationError('Passwords must match')
        return self.data['password']

    class Meta:
        model = User
        fields = ['username', 'password']


class EditProfileForm(forms.ModelForm):
    """ Form for editing an existing user """

    new_username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, help_text="Please provide password to apply changes")

    class Meta:
        model = User
        fields = ['new_username', 'password']


class ChangePasswordForm(forms.ModelForm):
    """ Form for changing password of an existing user """

    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_new_password(self):
        if self.data['new_password'] != self.data['confirm_password']:
            raise forms.ValidationError('Passwords must match')
        return self.data['new_password']

    class Meta:
        model = User
        fields = ['current_password', 'new_password']
