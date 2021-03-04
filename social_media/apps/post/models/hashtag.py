from django.db import models


class Tags(models.Model):
    name = models.CharField('پرجسب', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"
