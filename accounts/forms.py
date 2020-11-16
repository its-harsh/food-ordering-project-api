from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', min_length=8, max_length=128, widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
    )
    confirm_password = forms.CharField(
        label='Confirm Password', min_length=8, max_length=128, widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(message='The two password fields didn’t match.', code='INVALID_PASSWORD')
        password_validation.validate_password(password)
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text='Raw passwords are not stored, so there is no way to see this '
                  'user’s password, but you can change the password using '
                  '<a href="../password/">this form</a>.'
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
        ]

    def clean_is_superuser(self):
        is_superuser = self.cleaned_data.get('is_superuser')
        if is_superuser:
            self.cleaned_data['is_staff'] = True
            self.cleaned_data['is_active'] = True
        return is_superuser

    def clean_password(self):
        return self.initial['password']
