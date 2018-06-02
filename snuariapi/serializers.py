from rest_framework import serializers
from snuariapi.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    clubs_as_admin = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='club_admin')
    clubs_as_members = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='club_members')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'clubs_as_admin', 'clubs_as_members',)

class ClubListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'scope', 'category', 'introduction',)

class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)
        
class ClubDetailSerializer(serializers.HyperlinkedModelSerializer):
    admin = AttendanceSerializer(many=True, read_only=True)
    members = AttendanceSerializer(many=True, read_only=True)
    waitings = AttendanceSerializer(many=True, read_only=True)
    boards = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Club
        fields = ('id', 'name', 'admin', 'members', 'waitings', 'scope', 'category', 'introduction', 'boards', 'events',)

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
    name = serializers.CharField(source='profile.name', read_only=True)
    college = serializers.CharField(source='profile.college', read_only=True)
    major = serializers.CharField(source='profile.major', read_only=True)
    admission_year = serializers.IntegerField(source='profile.admission_year', read_only=True)
    clubs_as_admin = ClubListSerializer(many=True, source='club_admin')
    clubs_as_members = ClubListSerializer(many=True, source='club_members')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'college', 'major', 'admission_year', 'clubs_as_admin', 'clubs_as_members',)

class EventListSerializer(serializers.HyperlinkedModelSerializer):
    club = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'name', 'content', 'date', 'club',)

class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

class EventDetailSerializer(serializers.HyperlinkedModelSerializer):
    club = serializers.PrimaryKeyRelatedField(read_only=True)
    future_attendees = AttendanceSerializer(many=True, read_only=True)
    future_absentees = AttendanceSerializer(many=True, read_only=True)
    past_attendees = AttendanceSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'name', 'content', 'date', 'club', 'future_attendees', 'future_absentees', 'past_attendees', )
