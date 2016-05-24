from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from social.backends.google import GooglePlusAuth
# for loading Strategy - needed for authentication with access token
from social.apps.django_app.utils import load_strategy, load_backend


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

        curl command i use:
        ~~~~~~~~~~~~~~~~~~~
        curl -H "content-type: application/json"
        -d '{"backend": "google",
        "access_token":"ya29.CjHsAgbTcHDkvHdZFjHuvVIbJ6TR_PsvvsBuj-eztFfKSNNJI5iqFmNf8IQQlmnzv4_c"}'
        -X POST 127.0.0.1:8000/api/v1/auth/

        :param request:
        :return:
        """
        if "access_token" not in request.data or "backend" not in request.data:
            return Response("Bad request fields")
        try:


            client = GooglePlusAuth()
            client.strategy = load_strategy(request=request)
            # backend = load_backend(redirect_uri=None, strategy=client.strategy, name=request.data["backend"])
            userObj = client.do_auth(access_token=request.data['access_token'])
            resp = {"token": request.data["access_token"]}
            uid = self.is_new(userObj.email)
            if uid == 0 : # a new user
                resp["user_id"] = self.populate(fname=userObj.first_name, lname=userObj.last_name, email=userObj.email)
                resp["is_new"] = True
            else:
                resp["user_id"] = uid
                resp["is_new"] = False

            return Response(resp)
        except Exception, e:
            return Response(e.__str__())


    def populate(self, **kwargs):
        """
        method to populate new users into our DB
        :param kwargs: should contain fname, lname, email and later maybe other fields
        and dont forget to update model + migrate changes to DB bfore adding new fields
        :return:
        """
        u = User(fname=kwargs["fname"], lname=kwargs["lname"], email=kwargs["email"])
        u.save()
        return u.id

    def is_new(self, email):
        """
        returns an id for returning users and 0 for new ones
        :param email:
        :return: user_id
        """
        users = User.objects.all()
        for u in users:
            if email == u.email:
                return u.id
        return 0

