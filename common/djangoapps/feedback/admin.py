
from django.contrib import admin
from .models import CourseReview

# Register your models here.

#admin.site.register(CourseReview)
@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )
