from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class TermsConditions(models.Model):
    content = RichTextField()
