from django.contrib import admin
from .models import Album, Song, Classifier, Corpus

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Classifier)
admin.site.register(Corpus)
