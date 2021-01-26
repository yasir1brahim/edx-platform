from drf_extra_fields.fields import Base64ImageField

 Class MyImageModelSerializer(serializers.ModelSerializers):
      image=Base64ImageField()
      class meta:
         model=MyImageModel
         fields= ('data','image')
      def create(self, validated_data):
        image=validated_data.pop('image')
        data=validated_data.pop('data')
       return MyImageModel.objects.create(data=data,image=image)
