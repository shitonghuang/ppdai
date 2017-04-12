# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile, Comment, Notice
from django.utils import timezone


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="请输入文字标题.")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    time = forms.DateTimeField(widget=forms.HiddenInput(),initial=timezone.now)
    update_time = forms.DateTimeField(widget=forms.HiddenInput(),initial=timezone.now)
    author = forms.CharField(widget=forms.HiddenInput(), initial='author')
    url = forms.CharField(widget=forms.HiddenInput(), initial='www.baidu.com')
    sourcefile = forms.FileField(help_text="上传附件.")
    contents = forms.CharField(max_length=500,widget=forms.Textarea,help_text="请输入文字内容.")



    

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')



#3.22

class CommentForm(forms.ModelForm):
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    dislikes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    time = forms.DateTimeField(widget=forms.HiddenInput(),initial=timezone.now)
    author = forms.CharField(widget=forms.HiddenInput(), initial='author')
    contents = forms.CharField(max_length=500,widget=forms.Textarea,help_text="请输入文字内容.")
    

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Comment

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('page',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')


#3.22

class NoticeForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="请输入文字标题.")
    time = forms.DateTimeField(widget=forms.HiddenInput(),initial=timezone.now)
    contents = forms.CharField(max_length=500,widget=forms.Textarea,help_text="请输入文字内容.")


    class Meta:
        model = Notice
        fields = ('title','contents',)