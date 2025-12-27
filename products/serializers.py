from rest_framework import serializers
from products.models import Product, Category, Review



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
    class Meta:
        model = Product
        fields = 'id title price category'.split()
       

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