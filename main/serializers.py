from django.contrib.auth import get_user_model

from rest_framework import serializers


from main.models import Product, Response, UserProductRelation, Cart, ProductLikes


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ('id','creation_date')

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = ResponseSerializer(instance.comments.all(), many=True).data
        return rep


class AuthorSerializers(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username')

class ResponseSerializer(serializers.ModelSerializer):
    response = serializers.PrimaryKeyRelatedField(write_only=True,
                                                    queryset=Response.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    author = AuthorSerializers(read_only=True)
    # photo = serializers.ImageField(max_length=None, allow_empty_file=False)
    product_response = serializers.SerializerMethodField('paginated_product_response')
    liked_by_req_user = serializers.SerializerMethodField()
    class Meta:
        model = Response
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

    def get_number_of_responses(self,obj):
        return Response.objects.filter(product=obj).count()

    def get_liked_by_req_user(self,obj):
        user = self.context['request'].user
        return  user in obj.likes.all()

class UserProductRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = ('product', 'like', 'in_productmarks', 'rate')



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        return representation

class ProductlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLikes
        fields = '__all__'










