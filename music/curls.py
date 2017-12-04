from django.conf.urls import url
from . import cviews

app_name = 'classy'

urlpatterns = [
    url(r'^$', cviews.index, name='index'),
    url(r'^register/$', cviews.register, name='register'),
    url(r'^login_user/$', cviews.login_user, name='login_user'),
    url(r'^logout_user/$', cviews.logout_user, name='logout_user'),
    url(r'^(?P<classifier_id>[0-9]+)/$', cviews.detail, name='detail'),
    url(r'^stop_words_detail/(?P<classifier_id>[0-9]+)/$', cviews.stop_words_detail, name='stop_words_detail'),
    url(r'^(?P<corpus_id>[0-9]+)/favorite/$', cviews.favorite, name='favorite'),
    url(r'^corpus/(?P<filter_by>[a-zA_Z]+)/$', cviews.corpus, name='corpus'),
    url(r'^stop_words/$', cviews.stop_words, name='stop_words'),
    url(r'^create_classifier/$', cviews.create_classifier, name='create_classifier'),
    url(r'^(?P<classifier_id>[0-9]+)/classifier/$', cviews.classifier, name='classifier'),
    url(r'^(?P<classifier_id>[0-9]+)/trainer/$', cviews.trainer, name='trainer'),
    url(r'^(?P<classifier_id>[0-9]+)/upload_file/$', cviews.upload_file, name='upload_file'),
    url(r'^(?P<classifier_id>[0-9]+)/upload_stop_words/$', cviews.upload_stop_words, name='upload_stop_words'),
    url(r'^(?P<classifier_id>[0-9]+)/create_corpus/$', cviews.create_corpus, name='create_corpus'),
    url(r'^(?P<classifier_id>[0-9]+)/add_stop_words/$', cviews.add_stop_words, name='add_stop_words'),
    url(r'^(?P<classifier_id>[0-9]+)/delete_corpus/(?P<corpus_id>[0-9]+)/(?P<filter_by>[a-zA_Z]+)/$', cviews.delete_corpus, name='delete_corpus'),
    url(r'^(?P<classifier_id>[0-9]+)/delete_stop_words/(?P<stopwords_id>[0-9]+)/(?P<filter_by>[a-zA_Z]+)/$', cviews.delete_stop_words, name='delete_stop_words'),
    url(r'^(?P<classifier_id>[0-9]+)/favorite_classifier/$', cviews.favorite_classifier, name='favorite_classifier'),
    url(r'^(?P<classifier_id>[0-9]+)/delete_classifier/$', cviews.delete_classifier, name='delete_classifier'),
]
