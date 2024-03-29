from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    CreateAPIView,
    ListCreateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
    EmailSerializer,
    ResetUserPasswordSerializer,
    SubscriptionSerializer,
)
from authors.settings import EMAIL_HOST_USER, DEFAULT_FROM_EMAIL
from authors.apps.core.email_with_celery import SendEmail
from .chk_token import authcheck_token
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
    SocialAuthSerializer,
)

# social_auth
from social_core.exceptions import MissingBackend
from social_django.utils import load_backend, load_strategy
from social.backends.oauth import BaseOAuth1, BaseOAuth2


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get("user", {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serialized_email = serializer.data.get("email", None)
        user_email = get_user_model().objects.filter(email=serialized_email).first()
        current_site = get_current_site(request)
        SendEmail(
            template="verify_email.html",
            context={
                "user": user,
                "uid": urlsafe_base64_encode(force_bytes(user_email.pk)),
                "domain": current_site.domain,
                "token": authcheck_token.make_token(user_email),
            },
            subject="Authors Haven Verification",
            e_to=[
                user["email"],
            ],
            e_from=DEFAULT_FROM_EMAIL,
        ).send()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get("user", {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get("user", {})

        user_data = request.data.get("user", {})

        serializer_data = {
            "username": user_data.get("username", request.user.username),
            "email": user_data.get("email", request.user.email),
            "profile": {
                "bio": user_data.get("bio", request.user.profile.bio),
                "image": user_data.get("image", request.user.profile.image),
            },
        }

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyAPIView(APIView):
    """
    View for handling verification of user account, once the user signs up,
    a verification Token is set to the users email
    Arguments:
        APIView {[token, uuid]} -- [token is for verifying the user email and
        the uuid is for getting the user id]
    Returns:
        [type] -- [Http Response if the user was successfully verified or not]
    """

    def get(self, request, uidb64, token):
        try:
            uuid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uuid)
        except (User.DoesNotExist):
            user = None
        if user and authcheck_token.check_token(user, token):
            user.confirmed_user = True
            user.save()
            return HttpResponse("Email confirmed successfully")
        else:
            return HttpResponse("Email confirmation failed")


class UserForgetPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            serialized_email = serializer.data.get("email", None)
            user_email = get_user_model().objects.filter(email=serialized_email).first()
            current_site = get_current_site(request)
            reset_link = (
                "http://"
                + current_site.domain
                + "/api/auth/"
                + serializer.data["token"]
            )
            from django.conf import settings

            SendEmail(
                template="reset_pass.html",
                context={
                    "reset_url": reset_link,
                    "uid": urlsafe_base64_encode(force_bytes(user_email.pk)),
                    "domain": current_site.domain,
                    "email": serializer.data["email"],
                    "token": serializer.data["token"],
                },
                subject="Authors Haven Verification",
                e_to=[
                    serializer.data["email"],
                ],
                e_from=settings.EMAIL_HOST_USER,
            ).send()
            msg = f"Reset Link successfully sent to your Email"
            return Response({"message": msg}, status=status.HTTP_200_OK)
        msg = f"Password reset failed. Please check your email and try again"
        return Response({"message": msg}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordLinkView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = ResetUserPasswordSerializer

    def put(self, request, token):
        import json

        data = json.loads(json.dumps(request.data))
        data["token"] = token
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            msg = f"Password Successfull Reset"
            return Response({"message": msg}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribeAPIView(APIView):
    """
    Class that will enable user subscribe and unsubscribe from article mail notifications.

    Arguments:
        APIView {[request]} -- [contains all the payload]
    """

    permission_classes = (AllowAny,)
    serializer_class = SubscriptionSerializer

    def get(self, request, uuid):
        uuid = force_text(urlsafe_base64_decode(uuid))
        subscribe_user = User.objects.get(id=uuid)
        if subscribe_user.subscribed:
            subscribe_user.subscribed = False
            subscribe_user.save()
            return Response(
                {"message": "Successfully Unsubscribed"}, status=status.HTTP_200_OK
            )

        elif subscribe_user.subscribed == False:
            subscribe_user.subscribed = True
            subscribe_user.save()
            return Response(
                {"message": "Successfully Subscribed"}, status=status.HTTP_200_OK
            )
