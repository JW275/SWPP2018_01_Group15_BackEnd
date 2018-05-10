from rest_framework import serializers
from snuariapi.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'college', 'major', 'admission_year',)
        extra_kwargs = {
                'name': {'required': True, 'allow_blank': False},
            'college': {'required': True, 'allow_blank': False},
            'major': {'required': True, 'allow_blank': False},
            'admission_year': {'required': True},
        }

class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(source='profile.name')
    college = serializers.CharField(source='profile.college')
    major = serializers.CharField(source='profile.major')
    admission_year = serializers.IntegerField(source='profile.admission_year')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'college', 'major', 'admission_year',)

