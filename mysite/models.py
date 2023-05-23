from django.db import models


class PositiveWords(models.Model):
    positive_word = models.CharField(max_length=100)


class NegativeWords(models.Model):
    negative_word = models.CharField(max_length=100)


