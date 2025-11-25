from .models import *
from django import forms
from django.contrib.auth.hashers import check_password

class UserLoginForm(forms.Form):
    user_id = forms.CharField(max_length=8, label='User ID')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if not user_id or not password:
            try:
                user = UserProfile.objects.get(user_id=user_id)
                if not check_password(password, user.password):
                    raise forms.ValidationError("Invalid User ID or Password")
            except UserProfile.DoesNotExist:
                raise forms.ValidationError("Invalid User ID or Password")
        return cleaned_data
    
class CreateUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_id', 'user_name', 'email', 'phone', 'role', 'password']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_name', 'email', 'phone', 'role']
