from rest_framework import serializers
from main.models import Product, Response


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = ResponseSerializer(instance.comments.all(), many=True).data
        return rep


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'

class ResponseSerializer(serializers.ModelSerializer):
    response = serializers.PrimaryKeyRelatedField(write_only=True,
                                                    queryset=Response.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Response
        fields = ('id', 'text', 'user')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


