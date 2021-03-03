from django.db import models

from .post import Post
from .text import Text


class Comments(Text):
    class Meta(Text.Meta):
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        permissions = [
            ("confirm_comment", "تایید کردن"),
            ("active_comment", "فعال کردن")
        ]

    post = models.ForeignKey(Post, related_name="comment", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.confirm = False
        return super(Comments, self).save()

    def __str__(self):
        return self.post.title