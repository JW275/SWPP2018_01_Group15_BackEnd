from rest_framework import serializers
from snuariapi.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)
