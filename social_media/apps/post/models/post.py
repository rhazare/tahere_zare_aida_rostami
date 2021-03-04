from django.db import models
from django_extensions.db.fields import AutoSlugField

from .text import Text
from ..stop_word import tokenize_post_text
from .word import Word


class Post(Text):

    title = models.CharField('عنوان', max_length=50)
    slug = AutoSlugField(populate_from=['title',], unique=True, allow_unicode=True)
    image = models.ImageField(verbose_name='عکس پست', upload_to='uploads/post_image', null=True, blank=True) #faz 4 & pip install Pillow
    tags = models.ManyToManyField('Tags', verbose_name="برجسب ها", null=True, blank=True)

    class Meta(Text.Meta):
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
        permissions = [
            ("confirm_post", "تایید کردن"),
            ("active_post", "فعال کردن")
        ]

    def save(self, *args, **kwargs):
        """
        Before saving post I tokenize the word of text for
        more speed in searching in model Word

        """
        super().save(*args, **kwargs)
        for word in tokenize_post_text(self.text):
            new_word, create = Word.objects.get_or_create(word=word)
            if self not in new_word.post.all():
                new_word.post.add(self)
        return

    def __str__(self):
        return self.title