from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.conf import settings
from authors.apps.authentication.models import User


class BaseTest(APITestCase):
    client = APIClient

    def setUp(self):
        CELERY_TASK_ALWAYS_EAGER = True
        CELERY_TASK_EAGER_PROPOGATES = True
        self.SIGN_UP_URL = "/api/users/"
        self.PROFILE_URL = "/api/profiles/"
        self.LOG_IN_URL = "/api/users/login/"
        self.RESET_PASS = "/api/users/forgot_password/"

    user_cred = {
        "user": {
            "email": "jake@jake.jake",
            "username": "jake",
            "password": "J!ake123456",
        }
    }

    wrong_email = {"email": "wrongemail.werong"}

    correct_email = {
        "email": "jake@jake.jake",
    }

    no_email = {"eml": "wrongemail.wrong"}

    user_cred1 = {
        "user": {
            "email": "jake@jakerr.jake",
            "username": "jakerrrrrr",
            "password": "J!ake123456",
        }
    }

    user_cred2 = {
        "user": {
            "email": "jake123@jakerr.jake",
            "username": "jakerrrrrrrrr",
            "password": "J!ake123456",
        }
    }
    user_cred3 = {
        "user": {
            "email": "jakejakejake@gmail.com",
            "username": "jayajaya",
            "password": "J!ake123456",
        }
    }

    user_cred_wrong_pass = {
        "user": {
            "email": "jake@jake.jake",
            "username": "jake",
            "password": "some_fake_password",
        }
    }

    user_cred_no_email = {
        "user": {"email": "", "username": "jake", "password": "HelloWorldKen123"}
    }

    user_cred_no_username = {
        "user": {"email": "", "username": "", "password": "HelloWorldKen123"}
    }

    user_cred_no_details = {"user": {"email": "", "username": "", "password": ""}}

    testArticle = {
        "article": {
            "title": "How to feed your dragon",
            "description": "Wanna know how?",
            "body": "You don't believe?",
            "tagList": ["dragons", "training"],
        }
    }

    testArticle1 = {
        "article": {
            "title": "How to train your dragon",
            "description": "Ever wonder how?",
            "body": "You have to believe",
        }
    }
    user_cred_bio = {"user": {"bio": "I love testing"}}

    def register_user(self):
        return self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")

    def register_user_1(self):
        return self.client.post(self.SIGN_UP_URL, self.user_cred1, format="json")

    def register_user_2(self):
        return self.client.post(self.SIGN_UP_URL, self.user_cred2, format="json")

    def get_profile(self, username):
        return self.client.get(self.PROFILE_URL + str(username))

    def login_user(self):
        return self.client.post(self.LOG_IN_URL, self.user_cred, format="json")

    def login_user_1(self):
        return self.client.post(self.LOG_IN_URL, self.user_cred1, format="json")

    def login_user_2(self):
        return self.client.post(self.LOG_IN_URL, self.user_cred2, format="json")

    def get_token(self):
        response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
        response = self.client.post(
            reverse("authentication:user_login"), self.user_cred, format="json"
        )
        token = response.data["token"]
        return token

    def get_user2_token(self):
        response = self.client.post(self.SIGN_UP_URL, self.user_cred2, format="json")
        response = self.client.post(
            reverse("authentication:user_login"), self.user_cred2, format="json"
        )
        token = response.data["token"]
        return token

    def create_article(self, token, article):
        """
        Helper method to creates an article
        """
        return self.client.post(
            "/api/articles/",
            article,
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )

    def update_article(self, token, slug, article):
        """Helper method to update an article"""
        return self.client.put(
            "/api/articles/" + slug + "/update",
            article,
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )

    def delete_article(self, token, slug):
        """Helper method to delete an article"""

        return self.client.delete(
            "/api/articles/" + slug + "/delete",
            HTTP_AUTHORIZATION="Bearer " + token,
        )

    def favorite_article(self, token, slug):
        """
        Helper method to favorite an article
        """
        return self.client.post(
            "/api/articles/" + slug + "/favorite", HTTP_AUTHORIZATION="Bearer " + token
        )

    def unfavorite_article(self, token, slug):
        """
        Helper method to favorite an article
        """
        return self.client.delete(
            "/api/articles/" + slug + "/favorite", HTTP_AUTHORIZATION="Bearer " + token
        )

    def get_articles(self, token):
        """
        Helper method to get all articles after authentication

        """
        return self.client.get(
            "/api/articles/list", HTTP_AUTHORIZATION="Bearer " + token
        )

    def create_comment(self, comment):
        """
        Helper method to creates an article

        """

        token = self.get_token()
        return self.client.post(
            "/api/articles/how-to-feed-your-dragon/comments",
            comment,
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )

    def login_admin(self):
        User.objects.create_superuser(
            username="Teddy",
            email="teddykavooh@gmail.com",
            password="HelloWorldKen12!3",
        )

        data = {
            "user": {"email": "teddykavooh@gmail.com", "password": "HelloWorldKen12!3"}
        }

        return self.client.post(path="/api/users/login/", data=data, format="json")

    mutuba = {
        "user": {
            "email": "danielmutuba@gmail.com",
            "username": "Mutuba",
            "password": "J!ake123456",
        }
    }
    jason = {
        "user": {
            "email": "jason@gmail.com",
            "username": "Jason",
            "password": "J!ake123456",
        }
    }
    mercy = {
        "user": {
            "email": "mercy@gmail.com",
            "username": "Mercy",
            "password": "J!ake123456",
        }
    }
    loice = {
        "user": {
            "email": "Loice@gmail.com",
            "username": "Loice",
            "password": "J!ake123456",
        }
    }

    def get_mutuba_token(self):
        """
        returns token to be used in tests
        """
        response = self.client.post(self.SIGN_UP_URL, self.mutuba, format="json")
        response = self.client.post(
            reverse("authentication:user_login"), self.mutuba, format="json"
        )
        token = response.data["token"]
        return token

    def get_jason_token(self):
        """
        Returns token for 2nd user to be used in tests
        """
        response = self.client.post(self.SIGN_UP_URL, self.jason, format="json")
        response = self.client.post(
            reverse("authentication:user_login"), self.jason, format="json"
        )
        token = response.data["token"]
        return token

    def get_mercy_token(self):
        """
        Returns token for 3rd user to be used in tests
        """
        response = self.client.post(self.SIGN_UP_URL, self.mercy, format="json")
        response = self.client.post(
            reverse("authentication:user_login"), self.mercy, format="json"
        )
        token = response.data["token"]
        return token

    def get_loice_token(self):
        """
        Returns token for 4th user to be used in tests
        """
        response = self.client.post(self.SIGN_UP_URL, self.loice, format="json")
        response = self.client.post(
            reverse("authentication:user_login"), self.loice, format="json"
        )
        token = response.data["token"]
        return token
