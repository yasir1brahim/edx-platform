from rest_framework import serializers
from .models import Faq, FaqCategory


class FaqSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Faq
        fields = ('id', 'created', 'modified', 'question', 'answer', 'category_id', 'view_count')

class FaqCategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = FaqCategory
        fields = ('id', 'name', 'image')

class FaqCategoryTopSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta(object):
        model = FaqCategory
        fields = ('id', 'name', 'image')
    
    def get_image(self, category):
        request = self.context.get('request')
        image_url = category.image.url
        return request.build_absolute_uri(image_url)

class FaqDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ['id', 'created', 'modified', 'question', 'answer']

class FaqCategoryIDSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Faq
        fields = ('id', 'question')
