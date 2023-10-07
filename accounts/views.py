# import our packages
from rest_framework.response import Response
from .models import Profile, GameZoneUser
from .serializers import GamezoneUserSerializer, ProfileSeriaLizer
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
import uuid

class GamezoneUserViewset(ListCreateAPIView):
    queryset=GameZoneUser.objects.all().all()
    serializer_class=GamezoneUserSerializer
    permission_classes=[IsAuthenticated]
class DestroyUserView(DestroyAPIView):
    queryset=GameZoneUser.objects.all().all()
    serializer_class=GamezoneUserSerializer
    lookup_field="pk"
    permission_classes=[IsAuthenticated]

class UpdateUserView(UpdateAPIView):
    
    queryset=GameZoneUser.objects.all().all()
    serializer_class=GamezoneUserSerializer
    lookup_field="pk"
    permission_classes=[IsAuthenticated]

class RetrieveUSerView(RetrieveAPIView):
    queryset=GameZoneUser.objects.all().all()
    serializer_class=GamezoneUserSerializer
    lookup_field="pk"

class ProfileView(ViewSet):
    
    queryset=Profile.objects.all()
    permission_classes=[IsAuthenticated]

    # retrieve profile
    def retrieve(self, request, id=None):
        try:
            user=get_object_or_404(GameZoneUser, id=id)
            print(user.profile)
            if user.profile is None:
                return Response({
                    "message":"profile is blank"
                })
            serializer=ProfileSeriaLizer(user.profile)
            return Response(serializer.data)
        except:
            return Response({"error": "invalid user"})
    
    
    # create profile
    def create(self, request, id=None):
        data=request.data or request.FILES
        print(data['profile_pic'])
        user_profile=get_object_or_404(GameZoneUser, id=id)
        serializer=ProfileSeriaLizer(data=data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            profile=serializer.save()
            user_profile.profile=profile
            user_profile.save()
            return Response({
                "message": "profile created"
            })
        return Response({"error": "invalid user"})

    # edit proflle
    def edit_profile(self, request, *args, **kwargs):
        id=kwargs.get("id") or None
        user=get_object_or_404(GameZoneUser, id=id)

        if user:
            # access the user profile and posted data
            profile=user.profile
            serializer=ProfileSeriaLizer(instance=profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({
                "error":"data is invalid"
            })
        return Response({
                "error":"user does not exist"
            })


