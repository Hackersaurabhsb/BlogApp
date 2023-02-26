from django import forms
from .models import comment,Post,login
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.forms import ValidationError
from django.shortcuts import render,get_object_or_404,redirect
class Emailform(forms.Form):
    name=forms.CharField(max_length=50)
    froom=forms.EmailField(label="From")
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)


class Login_form(forms.ModelForm):
    class Meta:
        model=login
        fields='__all__'
        widgets={
            'password':forms.PasswordInput
        }
    def clean_username(self):
        uname=self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            return uname
        else:
            raise forms.ValidationError("Enter correct Username and Password")
    def clean_password(self):
        uname=self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            users=User.objects.get(username=uname)
            pword=self.cleaned_data.get('password')
            if users.check_password(pword):
                return pword

class commentform(forms.ModelForm):
    class Meta:
        model=comment
        fields=('name','email','body')
#model forms will automatically create forms for us 
#when we write model=modelname
#by default it selects all fields 
#to select spedific fields we use fields attribute
#we can also use exclude to exclude some of the fields
class make_blog_form(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','body','tags')


class SearchForm(forms.Form):
    query = forms.CharField()






class registration_form(forms.ModelForm):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','email']
        User.is_superuser=False
        User.is_staff=False
    def clean_password2(self):
        password1=self.cleaned_data.get("password1")
        password2=self.cleaned_data.get("password2")
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match. Please enter it again")
        return password2


#everything done only registration and login have to be checked

# class blog_edit_form(forms.Form):
#     # post=get_object_or_404(Post,pk=post_id)
#     title=forms.CharField(label='Title',initial=post.title)
#     body=forms.CharField(label='Body',initial=post.body)

    