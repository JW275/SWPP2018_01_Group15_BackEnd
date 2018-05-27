from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from snuariapi.models import *
from snuariapi.serializers import *
from snuariapi.services import *

from config import domain
import datetime

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            response = Response({'id':user.id}, status=200)
            response['Set-Cookie'] = 'auth={}; HttpOnly; Domain={}; PATH=/'.format(token.key, domain)
            return response
        else:
            return Response('', status=400)

class LogoutView(APIView):
    def post(self, request):
        response = Response('', status=200)
        response['Set-Cookie'] = 'auth=; HttpOnly; Domain={}; PATH=/; Expires={}'.format(domain, 'Tue, 27 Nov 1990 22:31:29 GMT')
        return response

class UserSelfView(APIView):
    def get(self, request):
        user = request.user
        if not user.is_anonymous:
            serializer = UserInfoSerializer(user)
            return Response(serializer.data)
        return Response('', status=400)

class UserDetailView(APIView):
    def get(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class ClubListView(APIView):
    def get(self, request):
        club = Club.objects.all()
        serializer = ClubListSerializer(club, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_anonymous: # if not a valid user
            return Response('user', status=400)
        serializer = ClubListSerializer(data=request.data)
        if serializer.is_valid():
            club = serializer.save()
            club.admin.add(request.user)
            return Response({'id':club.id})
        return Response('', status=400) # Something Wrong

class ClubDetailView(APIView):
    def get(self, request, pk=None):
        club = Club.objects.get(pk=pk)
        serializer = ClubDetailSerializer(club)
        return Response(serializer.data)

    def put(self, request, pk=None):
        club = Club.objects.get(pk=pk)
        serializer = ClubDetailSerializer(club, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('')
        return Response('', status=400)

    def delete(self, request, pk=None):
        club = Club.objects.get(pk=pk)
        club.delete()
        return Response('')

class ClubJoinView(APIView):
    # apply to club
    def post(self, request, pk=None):
        club = Club.objects.get(pk=pk)
        club.waitings.add(request.user)
        return Response('')
    
    # cancel apply
    def delete(self, request, pk=None):
        club = Club.objects.get(pk=pk)
        club.waitings.remove(request.user)
        return Response('')

class SignupView(APIView):
    def post(self, request):
        password = request.data.get('password', None)
        if password is None or password is '':
            return Response('', status=400)

        email = request.data.get('email', None)
        if email is not None:
            if not email.endswith('@snu.ac.kr'):
                return Response('', status=400)

        user_serializer = UserSerializer(data=request.data)
        profile_serializer = ProfileSerializer(data=request.data)
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            profile_serializer = ProfileSerializer(user.profile, data=request.data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                user.set_password(password)
                user.is_active = False
                user.save()

                # Set VerifyToken until there's no error
                while True:
                    try:
                        token = get_random_string(length=32)
                        vtoken = VerifyToken.objects.create(user=user, token=token)
                        send_verify_mail(token, user)
                        break
                    except:
                        continue

                return Response({'id':user.id})

        return Response('', status=400)

class VerifyView(APIView):
    def post(self, request):
        token = request.data.get('token', '')
        vtoken = VerifyToken.objects.filter(token=token).first()
        if vtoken is None:
            return Response('', status=400)

        vtoken.user.is_active = True
        vtoken.user.save()
        vtoken.delete()

        return Response('')
   
class BoardListView(APIView):
    def get(self, request):
        board = Board.objects.all()
        serializer = BoardListSerializer(board, many=True)
         return Response(serializer.data)

    def post(self, request):
        club_id = request.data.get('club_id', None)
        if club_id is None:
            return Response('club id is required', status=400)

        club = Club.objects.filter(id=club_id).first()
        if club is None:
            return Response('club does not exist', status=400)

        serializer = BoardListSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save()
            board.club = club
            board.save()
            return Response({'id':board.id})
        return Response('', status=400) # Something Wrong

class BoardDetailView(APIView):
    def get(self, request, pk=None):
        board = Board.objects.get(pk=pk)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)

    def put(self, request, pk=None):
        board = Board.objects.get(pk=pk)
        serializer = BoardDetailSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('')
        return Response('', status=400)

    def delete(self, request, pk=None):
        board = Board.objects.get(pk=pk)
        board.delete()
        return Response('')

class ArticleListView(APIView):
    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)

    def post(self, request):
        board_id = request.data.get('board_id', None)
        if board_id is None:
            return Response('board id is required', status=400)

        board = Board.objects.filter(id=board_id).first()
        if board is None:
            return Response('board does not exist', status=400)

        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save()
            article.writer = request.user
            article.board = board
            article.save()
            return Response({'id':article.id})
        return Response('', status=400) # Something Wrong

class ArticleDetailView(APIView):
    def get(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            article = serializer.save()
            article.updated_at = datetime.datetime.now()
            article.save()
            return Response('')
        return Response('', status=400)

    def delete(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response('')
      
class AccountingListView(APIView):
    def get(self, request):
        club_id = request.GET.get('club_id', None)
        if club_id is None:
            return Response('club id is required', status=400)
        club = Club.objects.filter(id=club_id).first()
        if club is None:
            return Response('club is not exist', status=400)
        account = club.club_accounting.all()
        serializer = AccountingSerializer(account, many=True)
        return Response(serializer.data)

    def post(self, request):
        club_id = request.data.get('club_id', None)
        if club_id is None:
            return Response('club id is required', status=400)
          
        club = Club.objects.filter(id=club_id).first()
        if club is None:
            return Response('club is not exist', status=400)
        serializer = AccountingSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.writer = request.user
            account.club = club
            account.save()
            return Response({"id": account.id})
        return Response(serializer.errors, status=400)

class AccountingDetailView(APIView):
    def get(self, request, pk=None):
        account = Accounting.objects.get(pk=pk)
        serializer = AccountingSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk=None):
        account = Accounting.objects.get(pk=pk)
        serializer = AccountingSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            account = serializer.save()
            account.updated_at = datetime.datetime.now()
            account.save()
            return Response('')
        return Response('', status=400)

    def delete(self, request, pk=None):
        account = Accounting.objects.get(pk=pk)
        account.delete()
        return Response('')
        
class AccountingStatisticView(APIView):
    def get(self, request, pk=None):
        club = Club.objects.filter(pk=pk).first()
        if club is None:
            return Response('club is not exist', status=400)
        account = club.club_accounting.all()

        start_from = request.GET.get('start_from', '1990-01-01')
        end_until = request.GET.get('end_until', datetime.datetime.now().strftime('%Y-%m-%d'))
        account = account.filter(date__range=(start_from, end_until))

        only = request.GET.get('only', 'all')
        if only == 'all':
            pass
        elif only == 'income':
            account = account.filter(is_income=True)
        elif only == 'outgo':
            account = account.filter(is_income=False)

        serializer = AccountingSerializer(account, many=True)
        total = 0
        for ac in account:
            if ac.is_income:
                total += ac.money
            else:
                total -= ac.money

        return Response({'total': total, 'accountings': serializer.data})

