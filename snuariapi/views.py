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
            club.members.add(request.user)
            club.admin.add(request.user)
            return Response({'id':club.id})
        return Response('', status=400) # Something Wrong
