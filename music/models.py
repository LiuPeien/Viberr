from django.contrib.auth.models import Permission, User
from django.db import models
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import os


class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title


class Classifier(models.Model):
    user = models.ForeignKey(User, default=1)
    classifier_name = models.CharField(max_length=50, unique=True)
    classifier_logo = models.FileField()
    classifier_labels = models.CharField(max_length=200, default='')
    is_favorite = models.BooleanField(default=False)

    model_dict = {
        'NB': OneVsRestClassifier(MultinomialNB()),
        'LR': OneVsRestClassifier(LogisticRegression(), n_jobs=-1),
        'SVM': OneVsRestClassifier(SVC(kernel='linear')),
        'MLKNN': OneVsRestClassifier(LogisticRegression(), n_jobs=-1),
        'MLRWR': OneVsRestClassifier(LogisticRegression(), n_jobs=-1),
    }

    def __str__(self):
        return self.classifier_name

    def get_model_path(self):
        return 'music/model/classifier' + str(self.id) + '.model'

    def add_corpus(self, category, text):
        corp = Corpus(classifier=self, category=category.strip().lower(),
                      text=text)
        corp.save()

    def train(self, classifier_model):
        stop_words = [sw.word for sw in Stopwords.objects.all()]

        pipe = Pipeline([
            ('vect', TfidfVectorizer(
                        token_pattern=r'[a-zA-Z]+|\s+|\_+|[^\w\d\s]',
                        stop_words=stop_words
                        )),
            ('clf', self.model_dict[classifier_model]),
            ])

        # 加载所有的文档
        corpus = self.corpus_set.all()
        text_list = [corp.corpus_text for corp in corpus]

        self.transform_label(corpus)
        # 进行训练
        self.trained_pipe = pipe.fit(text_list, self.label_matrix)
        joblib.dump(self.trained_pipe, 'music/model/classifier' + str(self.id) + '.model')

        return "Model done! You can make prediction now!"

    def predict(self, value):
        model_path = self.get_model_path()

        if os.path.exists(model_path) is True and self.classifier_labels is not '':
            self.trained_pipe = joblib.load(model_path)

            result = self.trained_pipe.predict([value])[0]
            classes_index = self.classifier_labels.split()

            labels = []
            for i in range(0, len(result)):
                if result[i] == 1:
                    labels.append(str(classes_index[i]))

            return labels
        else:
            return "Please train the classifier before making prediction!!!"

    def transform_label(self, corpus):
        labels_list = [corp.corpus_label for corp in corpus]

        # 标签分割
        labels = []

        for c in labels_list:
            labels.append(c.split())
        # 把多标签转换为一个矩阵
        mb = MultiLabelBinarizer()
        self.label_matrix = mb.fit_transform(labels)
        self.classifier_labels = " ".join(str(i) for i in mb.classes_)
        self.save(update_fields=['classifier_labels'])


class Corpus(models.Model):
    classifier = models.ForeignKey(Classifier, on_delete=models.CASCADE)
    corpus_title = models.CharField(max_length=100)
    corpus_text = models.TextField()
    corpus_label = models.CharField(max_length=100)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.corpus_title


class Stopwords(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.Stopwords_word
