from rest_framework import serializers
from snuariapi.models import *

class UserSimpleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    clubs_as_admin = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='club_admin')
    clubs_as_members = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='club_members')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'clubs_as_admin', 'clubs_as_members',)

class BoardListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name',)

class ClubListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'scope', 'category', 'introduction',)

class ClubDetailSerializer(serializers.HyperlinkedModelSerializer):
    admin = UserSimpleSerializer(many=True, read_only=True)
    members = UserSimpleSerializer(many=True, read_only=True)
    waitings = UserSimpleSerializer(many=True, read_only=True)
    boards = BoardListSerializer(many=True, read_only=True, source='board_club')
    class Meta:
        model = Club
        fields = ('id', 'name', 'admin', 'members', 'waitings', 'scope', 'category', 'introduction','boards',)

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
    clubs_as_admin = ClubListSerializer(many=True, source='club_admin')
    clubs_as_members = ClubListSerializer(many=True, source='club_members')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'college', 'major', 'admission_year', 'clubs_as_admin', 'clubs_as_members',)

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    writer = UserSimpleSerializer(read_only=True)
    article = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'writer', 'article',)
        
class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    writer = UserSimpleSerializer(read_only=True)
    board = serializers.PrimaryKeyRelatedField(read_only=True)
    comment = CommentSerializer(read_only=True, many=True, source='comment_article')
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'writer', 'board', 'comment',)

class ArticleSimpleSerializer(serializers.HyperlinkedModelSerializer):
    writer = UserSimpleSerializer(read_only=True)
    board = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'writer', 'board',)

class BoardDetailSerializer(serializers.HyperlinkedModelSerializer):
    articles = ArticleSimpleSerializer(read_only=True, many=True, source='article_board')
    class Meta:
        model = Board
        fields = ('id', 'name', 'articles',)

class AccountingSerializer(serializers.HyperlinkedModelSerializer):
    writer = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Accounting
        fields = ('id', 'created_at', 'updated_at', 'is_income', 'money', 'date', 'writer', 'content',)
