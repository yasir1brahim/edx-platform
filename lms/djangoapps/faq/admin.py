from django.contrib import admin
from .models import Faq, FaqCategory
from django import forms
from ckeditor.widgets import CKEditorWidget

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'category_id', 'view_count')
    pass

# class FaqAdminForm(forms.ModelForm):
#     answer = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = Faq

@admin.register(FaqCategory)
class FaqCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    # form = FaqAdminForm
    pass
