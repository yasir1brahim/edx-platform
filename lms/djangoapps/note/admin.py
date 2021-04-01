from django.contrib import admin
from .models import Note, NoteImages

# Note
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_id', 'title', 'description', 'student_id', 'is_public')
    pass


# NoteImages
@admin.register(NoteImages)
class NoteImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'note_id', 'image')
    pass

