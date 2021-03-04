from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField  # https://pypi.org/project/django-tinymce/


class Text(models.Model):
    """
    This is a abstract model that Post model and Comment model inheritance from this model (before faz4)
    """
    text = HTMLField(verbose_name='متن')
    confirm = models.BooleanField('تایید', default=False)
    date_pub = models.DateTimeField(verbose_name="تاریخ انتشار", auto_now_add=True)

    # user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s',
    #                          verbose_name='کاربر')
    # like = models.ManyToManyField(User, related_name="%(class)s_likedby", related_query_name="%(class)s_likedby",
    #                               blank=True, null=True)
    # dislike = models.ManyToManyField(User, related_name="%(class)s_dislikedby",
    #                                  related_query_name="%(class)s_dislikedby", blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def duration(self):
        return timezone.now() - self.date_pub
