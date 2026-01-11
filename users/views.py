from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from users.serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializer
from rest_framework.authtoken.models import Token
from random import randint
from users.models import ConfirmationCode
from rest_framework.exceptions import ValidationError


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username, 
                                    password=password, 
                                    is_active=False)
    
    code = ConfirmationCode.objects.create(code=randint(100000,999999), user=user)

    return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id})

@api_view(['POST'])
def confirmation_api_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    code = serializer.validated_data.get('code')

    try: 
        user = User.objects.get(username=username)
        confirm_code = ConfirmationCode.objects.get(user=user)
        if int(code) != confirm_code.code:
            raise ValidationError('Confirmation code is incorrect!')
        user.is_active = True
        user.save()
    except User.DoesNotExist:
        raise ValidationError('User does not exist!')
    
    return Response(status=status.HTTP_200_OK, data={'user_id': user.id,
                                                     'is_active': user.is_active})
    
    

@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED, data='Invalid username or password')
