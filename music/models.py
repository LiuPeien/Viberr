from django.contrib.auth.models import Permission, User
from django.db import models
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.pipeline import Pipeline


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
    classifier_name = models.CharField(max_length=100)
    classifier_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.classifier_name

    def add_corpus(self, category, text):
        corp = Corpus(classifier=self, category=category.strip().lower(),
                      text=text)
        corp.save()

    def train(self):
        pipe = Pipeline([
            ('vect', CountVectorizer(
                        token_pattern=r'[a-zA-Z]+|\s+|\_+|[^\w\d\s]',
                        )),
            ('clf', OneVsRestClassifier(LogisticRegression(), n_jobs=-1)),
            ])

        # 加载所有的文档
        corpus = self.corpus_set.all()
        text_list = [corp.corpus_text for corp in corpus]
        labels_list = [corp.corpus_label for corp in corpus]

        # 标签分割
        labels = []
        for c in labels_list:
            labels.append(c.split())

        # 把多标签转换为一个矩阵
        mb = MultiLabelBinarizer()
        label_matrix = mb.fit_transform(labels)
        self.classes_index = mb.classes_

        # 进行训练
        self.trained_pipe = pipe.fit(text_list, label_matrix)

    def predict(self, value):
        result = self.trained_pipe.predict([value])[0]
        labels = ""

        for i in range(0, len(result)):
            if result[i] == 1:
                labels = labels + " " + self.classes_index[i]

        return labels


class Corpus(models.Model):
    classifier = models.ForeignKey(Classifier, on_delete=models.CASCADE)
    corpus_title = models.CharField(max_length=100)
    corpus_text = models.TextField()
    corpus_label = models.CharField(max_length=100)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.corpus_title