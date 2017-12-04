from django.contrib import admin
from .models import *

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Classifier)
admin.site.register(Corpus)
admin.site.register(Stopwords)
