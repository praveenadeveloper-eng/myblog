from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Categories,Article,Comment


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

class LoginForm(forms.Form):
     username = forms.CharField(
        max_length=150,
        label="Username",
        required=True
    )
     password= forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        required=True
    )


class CategoryForm(forms.ModelForm):

    class Meta:
        model=Categories
        fields ='__all__'

class ArticleForm(forms.ModelForm):

    class Meta:
        model=Article
        fields = ('title','category','featured_image','short_description','blogbody','status','is_feature')

class AddUserForm(UserCreationForm):
    class Meta:
        model= User
        fields = ('username','first_name','last_name','email','is_active','is_staff','groups','user_permissions')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('username','first_name','last_name','email','is_active','is_staff','groups','user_permissions')


