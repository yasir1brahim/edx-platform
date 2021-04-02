from django.db.models import fields
from rest_framework import serializers
from .models import Note, NoteImages

class NoteSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Note
        fields = '__all__'


class MyNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'is_public')


class MyNoteImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta(object):
        model = NoteImages
        fields = ('id', 'note_id', 'image')

    def get_image(self, category):
        request = self.context.get('request')
        image_url = category.image.url
        return request.build_absolute_uri(image_url)


