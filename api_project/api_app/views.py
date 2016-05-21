from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from social.backends.google import GooglePlusAuth
from social.strategies.django_strategy import DjangoStrategy
# Create your views here.

class UsersView(APIView):

    def get(self, request):
        """

        :return: a json of all users that are in DB
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)



class RegisterView(APIView):

    def is_new(self, email):
        users = User.objects.all()
        for u in users:
            if email == u.email:
                return False
        return True

    def post(self, request):
        """
        add a user , fields taken from request
        :param request:
        :return:
        """
        data = request.data
        fname = data['fname']
        lname = data['lname']
        email = data['email']
        u = User(fname=fname, lname=lname, email=email)
        if self.is_new(email):
            u.save()
        else:
            return Response("User already in DB")

        return Response("User was added to DB")

class GoogleAuthView(APIView):

    def post(self, request):
        """
        Authenticate user by using an access token and get his profile data to store in DB
        if its a new user.
        :param request:
        :return:
        """
        data = request.data # json
        # backend = data['backend']
        # access_token = data['access_token']
        client = GooglePlusAuth()
        client.data = data
        client.auth_complete_params()
        # client.strategy = DjangoStrategy()
        # client.do_auth(data['access_token'])
        # info = client.auth_complete()
        return Response("fff")