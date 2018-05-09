from rest_framework import serializers
from snuariapi.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # club = serializers.PrimaryKeyRelatedField(source='club_members', many=True, read_only=True)
    clubs_as_admin = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='club_admin')
    clubs_as_member = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='club_members')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'clubs_as_admin', 'clubs_as_members',)

class ClubListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'scope', 'category', 'introduction',)

class ClubDetailSerializer(serializers.HyperlinkedModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    waitings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Club
        fields = ('id', 'name', 'admin', 'members', 'waitings', 'scope', 'category', 'introduction',)
