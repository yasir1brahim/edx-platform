import urllib
import os
from django.db import models
from django.core.files import File
from django.utils import timezone
from ckeditor.fields import RichTextField
# from django_ckeditor_5.fields import CKEditor5Field

# faq
class Faq(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
    question = models.CharField(max_length=1200)
    answer = RichTextField(blank=True)
    category_id = models.ForeignKey('FaqCategory', on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'Faq'
        verbose_name_plural = 'Faq'

    def as_json(self):
        return dict(
            id = self.id,
            question = self.question
        )

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Faq, self).save(*args, **kwargs)

    def _str_(self):
        return self.question   


    def _unicode_(self):
        return u'%s %s %d %d' % (self.question, self.answer, self.category_id, self.view_count)


    @property
    def category_name(self):
        return self.category_id.name


# faq_category
class FaqCategory(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='faq_images/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = 'FaqCategory'
        verbose_name_plural = 'FaqCategory'

    def _unicode_(self):
        return '%s' % (self.name)

    def _str_(self):
        return self.name

    def as_json(self):
        return dict(
            id = self.id,
            name = self.name
        )

    def cache(self):
        """Store image locally if we have a URL"""

        if self.url and not self.image:
            result = urllib.urlretrieve(self.url)
            self.photo.save(
                    os.path.basename(self.url),
                    File(open(result[0], 'rb'))
                    )
            self.save()
