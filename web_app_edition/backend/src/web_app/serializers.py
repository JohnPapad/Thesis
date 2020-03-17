
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import User

from .models import NMM_ELO_Rating

class UserSerializerWithToken(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    username = serializers.CharField(
            required=True,max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    
    password = serializers.CharField(required=True,min_length=8,write_only=True)
    
    first_name =serializers.CharField(required=True,min_length=2)
    last_name =serializers.CharField(required=True,min_length=2)

    token = serializers.SerializerMethodField()
    
    def get_token(self, object):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(object)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            password = validated_data['password'],
            email = validated_data['email'],
        )
        user.save()
        user_elo = NMM_ELO_Rating.objects.create_elo(user)
        user_elo.save()
        return user
    
    class Meta:
        model = User
        fields = ('token','id', 'username', 'email','password', 'first_name',
        'last_name')

class CheckUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    username = serializers.CharField(
            max_length=32,required=False,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    class Meta:
        model = User
        fields = ('username', 'email',)

class GetIDUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username',)