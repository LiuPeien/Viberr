from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import *
from .models import Classifier, Corpus, Stopwords

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_classifier(request):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        form = ClassifierForm(request.POST or None, request.FILES or None)
        user = request.user
        if form.is_valid():
            classifier = form.save(commit=False)
            classifier.user = request.user
            classifier.classifier_name = form.cleaned_data['classifier_name']

            for c in Classifier.objects.filter(user=request.user):
                if c.classifier_name == form.cleaned_data['classifier_name']:
                    context = {
                        'classifier': classifier,
                        'form': form,
                        'error_message': 'WARNING: You have created classifier with the same name!',
                        'user': user,
                    }
                    return render(request, 'classy/create_classifier.html', context)

            # 判断文件格式是否正确
            classifier.classifier_logo = request.FILES['classifier_logo']
            file_type = classifier.classifier_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'classifier': classifier,
                    'form': form,
                    'error_message': 'WARNING: Image file must be PNG, JPG, or JPEG!',
                    'user': user,
                }
                return render(request, 'classy/create_classifier.html', context)
            classifier.save()
            return render(request, 'classy/detail.html', {'classifier': classifier})
        context = {
            "form": form,
            'user': user,
        }
        return render(request, 'classy/create_classifier.html', context)


def create_corpus(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        form = CorpusForm(request.POST or None)
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        user = request.user

        if form.is_valid():
            corpus = form.save(commit=False)
            corpus.classifier = classifier
            corpus.corpus_text = form.cleaned_data['corpus_text']
            corpus.corpus_label = form.cleaned_data['corpus_label']

            corpus.save()
            return render(request, 'classy/detail.html', {'classifier': classifier, 'user': user})
        context = {
            'classifier': classifier,
            'form': form,
            'user': user,
        }
        return render(request, 'classy/create_corpus.html', context)


def add_stop_words(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        form = StopwordsForm(request.POST or None)
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        user = request.user

        if form.is_valid():
            stopwords = form.save(commit=False)
            stopwords.classifier = classifier
            stopwords.word = form.cleaned_data['word']

            stopwords.save()
            return render(request, 'classy/stopwords_detail.html', {'classifier': classifier, 'user': user})
        context = {
            'classifier': classifier,
            'form': form,
            'user': user,
        }
        return render(request, 'classy/add_stopwords.html', context)


def delete_classifier(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        classifier = Classifier.objects.get(pk=classifier_id)
        classifier.delete()
        classifier = Classifier.objects.filter(user=request.user)
        user = request.user
        return render(request, 'classy/index.html', {'classifier': classifier, 'user': user})


def delete_corpus(request, classifier_id, corpus_id, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        user = request.user
        corpus = Corpus.objects.get(pk=corpus_id)
        corpus.delete()

        if filter_by == 'detail':
            return render(request, 'classy/detail.html', {'classifier': classifier, 'user': user})
        else:
            context = {
                'classifier': classifier,
                'filter_by': filter_by,
                'user': user,
            }
            return render(request, 'classy/corpus.html', context)


def delete_stop_words(request, classifier_id, stopwords_id, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        user = request.user
        stopwords = Stopwords.objects.get(pk=stopwords_id)
        stopwords.delete()

        if filter_by == 'detail':
            return render(request, 'classy/stopwords_detail.html', {'classifier': classifier, 'user': user})
        else:
            context = {
                'classifier': classifier,
                'filter_by': filter_by,
                'user': user
            }
            return render(request, 'classy/stopwords.html', context)


def detail(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        user = request.user
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        return render(request, 'classy/detail.html', {'classifier': classifier, 'user': user})


def stop_words_detail(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        user = request.user
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        return render(request, 'classy/stopwords_detail.html', {'classifier': classifier, 'user': user})


def favorite(request, corpus_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        corpus = get_object_or_404(Corpus, pk=corpus_id)
        try:
            if corpus.is_favorite:
                corpus.is_favorite = False
            else:
                corpus.is_favorite = True
            corpus.save()
        except (KeyError, Corpus.DoesNotExist):
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': True})


def favorite_classifier(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        try:
            if classifier.is_favorite:
                classifier.is_favorite = False
            else:
                classifier.is_favorite = True
            classifier.save()
        except (KeyError, Classifier.DoesNotExist):
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        classifier = Classifier.objects.filter(user=request.user)
        corpus_results = Corpus.objects.all()
        query = request.GET.get("q")
        user = request.user
        if query:
            classifier = classifier.filter(
                Q(classifier_name__icontains=query)
            ).distinct()
            corpus_results = corpus_results.filter(
                Q(corpus_title__icontains=query)
            ).distinct()
            return render(request, 'classy/index.html', {
                'classifiers': classifier,
                'corpuses': corpus_results,
            })
        else:
            return render(request, 'classy/index.html', {'classifiers': classifier, 'user': user})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'classy/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                classifier = Classifier.objects.filter(user=request.user)
                return render(request, 'classy/index.html', {'classifiers': classifier, 'user': user})
            else:
                return render(request, 'classy/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'classy/login.html', {'error_message': 'Invalid login'})
    return render(request, 'classy/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                classifier = Classifier.objects.filter(user=request.user)
                return render(request, 'classy/index.html', {'classifier': classifier, 'user': user})
    context = {
        "form": form,
    }
    return render(request, 'classy/register.html', context)


def corpus(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        user = request.user
        try:
            corpus_ids = []
            for classifier in Classifier.objects.filter(user=request.user):
                for corpus in classifier.corpus_set.all():
                    corpus_ids.append(corpus.pk)
            users_corpus = Corpus.objects.filter(pk__in=corpus_ids)
            if filter_by == 'favorites':
                users_corpus = users_corpus.filter(is_favorite=True)
        except Classifier.DoesNotExist:
            users_corpus = []
        return render(request, 'classy/corpus.html', {
            'corpus_list': users_corpus,
            'filter_by': filter_by,
            'user': user,
        })


def stop_words(request):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        user = request.user
        try:
            stop_words_ids = []
            for classifier in Classifier.objects.filter(user=request.user):
                for sw in classifier.stopwords_set.all():
                    stop_words_ids.append(sw.pk)
            stop_words_list = Stopwords.objects.filter(pk__in=stop_words_ids)
        except Classifier.DoesNotExist:
            stop_words_list = []
        return render(request, 'classy/stopwords.html', {
            'stop_words_list': stop_words_list,
            'user': user,
        })


def trainer(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        form = ModelChoiceForm(request.POST or None)
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        user = request.user
        train_message = ""

        if form.is_valid():
            classifier_model = form.cleaned_data['classifier_model']
            train_message = classifier.train(classifier_model)

        context = {
            'train_message': train_message,
            'classifier': classifier,
            'form': form,
            'user': user,
        }
        return render(request, 'classy/trainer.html', context)


def classifier(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        form = PredictionForm(request.POST or None)
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        user = request.user
        prediction = ""

        if form.is_valid():
            corpus_text = form.cleaned_data['corpus_text']
            prediction = classifier.predict(corpus_text)

        context = {
            'prediction': prediction,
            'classifier': classifier,
            'form': form,
            'user': user,
        }
        return render(request, 'classy/classifier.html', context)


def upload_file(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        form = UploadFileForm(request.POST or None, request.FILES or None)
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        user = request.user

        if form.is_valid():
            print('file received!')
            file = request.FILES['file']

            for chunk in file.chunks():
                csv_data = chunk.decode()
                csv_rows = csv_data.split('\n')
                for i in range(1, len(csv_rows)):
                    row_values = csv_rows[i].split(',')
                    corp = Corpus(classifier=classifier,
                                  corpus_title=row_values[0],
                                  corpus_text=row_values[1],
                                  corpus_label=row_values[2])
                    corp.save()
            return render(request, 'classy/detail.html', {'classifier': classifier, 'user': user})

        context = {
            'classifier': classifier,
            'form': form,
            'user': user,
        }
        return render(request, 'classy/upload_file.html', context)


def upload_stop_words(request, classifier_id):
    if not request.user.is_authenticated():
        return render(request, 'classy/login.html')
    else:
        form = UploadFileForm(request.POST or None, request.FILES or None)
        classifier = get_object_or_404(Classifier, pk=classifier_id)
        user = request.user

        if form.is_valid():
            print('file received!')
            file = request.FILES['file']

            for chunk in file.chunks():
                csv_data = chunk.decode()
                csv_rows = csv_data.split('\n')
                for i in range(1, len(csv_rows)):
                    row_values = csv_rows[i].split(',')
                    stopwords = Stopwords(classifier=classifier,
                                          word=row_values[0])
                    stopwords.save()

            return render(request, 'classy/stopwords_detail.html', {'classifier': classifier, 'user': user,})

        context = {
            'classifier': classifier,
            'form': form,
            'user': user,
        }
        return render(request, 'classy/upload_stopwords.html', context)