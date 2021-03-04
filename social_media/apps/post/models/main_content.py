from django.db import models

class MainContent(models.Model):
    """
    This model describe a main content of site
    Who is this page for?؟ This model answer this question
    Slide show index template using the data of this model.
    """
    class Meta:
        verbose_name = 'نام کاربری'
        verbose_name_plural = "نام کاربری"

    image = models.ImageField(verbose_name='عکس پروفایل', upload_to='uploads/slide_show')
    website =models.URLField(max_length=200, db_index=True, unique=True, blank=True) #faz3
    title = models.CharField('نام کاربری', max_length=200)
    short_description = models.CharField('بیو', max_length=300) #faz3