from django import forms
from django.contrib.auth.models import User

from .models import *


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ClassifierForm(forms.ModelForm):

    class Meta:
        model = Classifier
        fields = ['user', 'classifier_name', 'classifier_logo']


class CorpusForm(forms.ModelForm):

    class Meta:
        model = Corpus
        fields = ['corpus_title', 'corpus_text', 'corpus_label']


class StopwordsForm(forms.ModelForm):

    class Meta:
        model = Stopwords
        fields = ['word']


class PredictionForm(forms.ModelForm):

    class Meta:
        model = Corpus
        fields = ['corpus_text']


class UploadFileForm(forms.Form):
    classifier_name = forms.CharField(max_length=50)
    file = forms.FileField()


class UploadStopWordsFileForm(forms.Form):
    file = forms.FileField()


class ModelChoiceForm(forms.Form):
    MODLE_LIST = (
        ('NB', 'Naive Bayes'),
        ('LR', 'Logistic Regression'),
        ('SVM', 'Support vector machine'),
        ('MLKNN', 'ML-KNN'),
        ('MLRWR', 'ML-RWR'),
    )
    classifier_model = forms.ChoiceField(choices=MODLE_LIST, label='Choose Model')