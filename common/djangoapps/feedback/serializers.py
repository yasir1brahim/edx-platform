from .models import CourseReview
from rest_framework import serializers

class CourseReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseReview
        fields = '__all__'
        # exclude = ['shipper']
