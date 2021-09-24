from django import forms

from .models import Topic, Entry, Profile


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'header_image']
        labels = {'text': '', "header_image": " Dodaj ikonę do tematu:"}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'': forms.Textarea(attrs={'cols': 80})}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'insta_url', 'pinterest_url']