from django.db import models


class Word(models.Model):
    """
    This is model that contain the word of the post
    after tookenize for searching in word of post text
    """
    class Meta:
        #Create index on word because of a lot of query on word
        indexes = [
            models.Index(fields=['word']),
        ]

    word = models.CharField(max_length=50, verbose_name='کلمه')
    post = models.ManyToManyField(to='Post', null=True, related_name='word')

    def __str__(self):
        return self.word