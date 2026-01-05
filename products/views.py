from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from products.models import Category, Product, Review
from products.serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, ReviewListSerializer, ReviewDetailSerializer, ProductReviewSerializer

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.prefetch_related('products').all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        name = request.data.get('name')

        category = Category.objects.create(name=name)
    
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'category not found!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategorySerializer(category, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        data = ProductListSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )
    
    return Response(status=status.HTTP_201_CREATED, 
                    data=ProductDetailSerializer(product).data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error: product not found!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewListSerializer(reviews, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        stars = request.data.get('stars')
        text = request.data.get('text')
        product_id = request.data.get('product_id')

        review = Review.objects.create(
            stars=stars,
            text=text,
            product_id=product_id
        )

    return Response(status=status.HTTP_201_CREATED,
                    data=ReviewDetailSerializer(review).data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error: review not found!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        review.stars = request.data.get('stars')
        review.text = request.data.get('text')
        review.product_id = request.data.get('product_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def product_list_review_api_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    data = ProductReviewSerializer(products, many=True).data
    return Response(data=data)