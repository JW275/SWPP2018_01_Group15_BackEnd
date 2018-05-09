from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from snuariapi.models import *
from snuariapi.serializers import *

from config import domain

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
        print(request.user)
        if request.user.is_anonymous: # if not a valid user
            return Response('user', status=400)
        serializer = ClubListSerializer(data=request.data)
        if serializer.is_valid():
            club = serializer.save()
            club.members.add(request.user)
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


