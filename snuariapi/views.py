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

from datetime import datetime
import pytz

utc = pytz.UTC
now = datetime.now().replace(tzinfo=utc)

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

class EventListView(APIView):
    def get(self, request):
        time = request.GET.get('need', None)
        clubid = request.GET.get('clubid', None)
        if clubid == None:
            return Response('', status=400)
        if time == None:
            events = Event.objects.filter(club = clubid)
        elif time == 'future':
            events = Event.objects.filter(club = clubid).filter(date__gte = (now))
        elif time == 'past':
            events = Event.objects.filter(club = clubid).filter(date__lte = (now))
        else:
            return Response('', status=400)
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_anonymous:
            return Response('user', status=400)
        club_id = request.data.get('club', None)
        club = Club.objects.get(pk=club_id)
        if club is None:
            return Response('club id is required', status=400)
        serializer = EventListSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            event.club = club
            event.save()
            time = None
            event_date = event.date
            if event_date >= now:
                time = 'future'
            else:
                time = 'past'
            serializer = EventListSerializer(event)
            return Response({'event': serializer.data, 'time': time})   #is this right?
        return Response('', status=400)

class EventDetailView(APIView):
    def get(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        serializer = EventDetailSerializer(event, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        serializer = EventDetailSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('')
        return Response('', status=400)

    def delete(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response('')

class EventFutureAttendeeView(APIView):
    def post(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event.future_attendees.add(request.user)
        event.future_absentees.remove(request.user)
        event.save()
        return Response({
            'id': request.user.id,
            'username': request.user.username
        })

    def delete(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event.future_attendees.remove(request.user)
        event.save()
        return Response({
            'id': request.user.id,
            'username': request.user.username
        })

class EventFutureAbsenteeView(APIView):
    def post(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event.future_absentees.add(request.user)
        event.future_attendees.remove(request.user)
        event.save()
        return Response({
            'id': request.user.id,
            'username': request.user.username
        })

    def delete(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event.future_absentees.remove(request.user)
        event.save()
        return Response({
            'id': request.user.id,
            'username': request.user.username
        })

class EventPastAttendeeView(APIView):
    def post(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event.past_attendees.add(request.user)
        event.save()
        return Response({
            'id': request.user.id,
            'username': request.user.username
        })

    def delete(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event.past_attendees.remove(rquest.user)
        event.save()
        return Response({
            'id': request.user.id,
            'username': request.user.username
        })

class EventStatisticView(APIView):
    def get(self, request, pk=None):
        event = Event.objects.filter(club=pk)
        user_id = request.GET.get('user', None)
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response('Invalid user id', status=400)
        # calculate absent count
        plan = event.filter(future_attendees=user)
        real = plan.filter(past_attendees=user)
        absent_count = len(plan) - len(real)
        # calculate attendence rate
        final = event.filter(past_attendees=user)
        attendence_rate = len(final) / len(event)
        return Response({'attendence_rate': attendence_rate, 'absent_count': absent_count})

