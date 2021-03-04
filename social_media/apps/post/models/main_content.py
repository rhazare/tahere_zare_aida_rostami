from django.db import models


class MainContent(models.Model):
    """
    faz3
    This model describe a main content of site
    Who is this page for?؟ This model answer this question
    Slide show index template using the data of this model.
    """

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = "پروفایل"

    title = models.CharField(verbose_name='نام و نام خانوادگی', max_length=200, blank=True)
    image = models.ImageField(verbose_name='عکس پروفایل', upload_to='uploads/slide_show', blank=True)
    website = models.URLField(verbose_name='وبسایت', max_length=200, db_index=True, blank=True)
    short_description = models.CharField(verbose_name='بیو', max_length=300, blank=True)
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(verbose_name='جنسیت', choices=GENDER_CHOICES, blank=True)
