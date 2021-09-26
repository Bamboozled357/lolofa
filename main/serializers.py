from rest_framework import serializers
from main.models import Category, Product, ProductImage, Response


class ListProductSerializer(serializers.ModelSerializer):  #ok
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):  #ok
    class Meta:
        model = Product
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, validated_data, instance):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().update(validated_data)


class DetailProductSerializer(serializers.ModelSerializer):  #ok
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = ResponseSerializer(instance.comments.all(), many=True).data
        return rep


class ResponseSerializer(serializers.ModelSerializer):
    response = serializers.PrimaryKeyRelatedField(write_only=True,
                                                    queryset=Response.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Response
        fields = ('id', 'text', 'user', 'response')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


