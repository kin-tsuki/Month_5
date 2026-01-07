from rest_framework import serializers
from products.models import Product, Category, Review
from rest_framework.exceptions import ValidationError



class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, category):
        products = category.products.all()
        if products:
            return products.count()
        else:
            return 0


class ProductListSerializer(serializers.ModelSerializer): 
    category = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = 'id title price category'.split()
       
    def get_category(self, product):
        return product.category.name

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True)
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = 'title reviews rating'.split()

    def get_rating(self, product):
        reviews = product.reviews.all()
        if reviews:
            stars = sum(review.stars for review in reviews)
            rating = round(stars / reviews.count(), 1)
            return rating
        else:
            return 0


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=255)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=255)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=8,decimal_places=2)
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id
    
class ReviewValidateSerializer(serializers.Serializer):
    stars = serializers.IntegerField(min_value=1, max_value=5, default=4)
    text = serializers.CharField(required=False, min_length=2, max_length=1000)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')
        return product_id
