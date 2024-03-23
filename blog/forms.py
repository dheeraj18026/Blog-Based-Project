from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from blog.models import Post

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control my-2'}))
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'form-control my-2'}))
    class Meta:
        model = User
        fields=['username','first_name','last_name','email']
        labels = {'username':'User ID','first_name':'First Name','last_name':'Last Name','email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control my-2'}),
                   'first_name':forms.TextInput(attrs={'class':'form-control my-2'}),
                   'last_name':forms.TextInput(attrs={'class':'form-control my-2'}),
                   'email':forms.TextInput(attrs={'class':'form-control my-2'})}


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control my-2'}))
    password = forms.CharField(label=_('Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control my-2'}))
   


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','desc']
        labels = {'title':'Title','desc':'Description'}
        widgets = {'title':forms.TextInput(attrs={'class':'form-control my-2'}),
                   'desc':forms.Textarea(attrs={'class':'form-control my-2'})}
