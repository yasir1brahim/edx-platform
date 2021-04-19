import os
import urllib

from django.core.files.base import File
from openedx.core.djangoapps.django_comment_common.comment_client.models import Model
from django.db import models
from django.contrib.auth.models import User
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from django.utils import timezone

# Create your models here.


class Note(models.Model):

    course_id = models.ForeignKey(CourseOverview, db_constraint=False, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=1500)
    description = models.TextField()
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Note'

    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.description, self.is_public)

    def __str__(self):
        return str(self.id)

    def as_json(self):
        return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            is_public = self.is_public,
        )
    def get_date(self):
        return self.modified.date()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Note, self).save(*args, **kwargs)

class NoteImages(models.Model):

    note_id = models.ForeignKey('Note', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='note_images/%Y/%m/%d/', null=True, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    class Meta:
        verbose_name = 'NoteImages'
        verbose_name_plural = 'NoteImages'

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(NoteImages, self).save(*args, **kwargs)

    def cache(self):
        """Store image locally if we have a URL"""

        if self.url and not self.image:
            result = urllib.urlretrieve(self.url)
            self.image.save(
                    os.path.basename(self.url),
                    File(open(result[0], 'rb'))
                    )
            self.save()
    

