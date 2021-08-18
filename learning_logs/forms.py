from django import forms

from .models import Topic, Entry


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