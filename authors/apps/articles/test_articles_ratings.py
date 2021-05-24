from ..base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status
import json


class ArticleTestCase(BaseTest):
    """
    Class implements tests for artcles
    """

    def rate_article(self, token, slug, rate):
        """
        Helper method to creates an article
        """
        return self.client.post(
            "/api/articles/" + slug + "/rate",
            rate,
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )

    def test_cannot_rate_own_article(self):
        """
        Test an article can be searched by title
        and returned successfully

        """

        self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
        login_response = self.client.post(
            reverse("authentication:user_login"), self.user_cred, format="json"
        )
        token = login_response.data["token"]

        response = self.create_article(token, self.testArticle)
        slug = response.data["slug"]
        rate = {"rate": {"rating": 5}}
        response = self.rate_article(token, slug, rate)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_can_rate_article_successfully(self):
        """
        Tests whether a user can rate an article successfully
        """

        self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
        login_response = self.client.post(
            reverse("authentication:user_login"), self.user_cred, format="json"
        )
        token = login_response.data["token"]

        response = self.create_article(token, self.testArticle)

        slug = response.data["slug"]
        response = self.client.post(self.SIGN_UP_URL, self.user_cred1, format="json")

        rater_login_response = self.client.post(
            reverse("authentication:user_login"), self.user_cred1, format="json"
        )

        rater_token = rater_login_response.data["token"]

        rate = {"rate": {"rating": 5, "note": "I loved the dragons story"}}

        response = self.rate_article(rater_token, slug, rate)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_cannot_rate_article_with_non_integer_value(self):
        """
        Tests whether a user can rate an article with non integer rate value
        """

        self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
        login_response = self.client.post(
            reverse("authentication:user_login"), self.user_cred, format="json"
        )
        author_token = login_response.data["token"]

        response = self.create_article(author_token, self.testArticle)
        slug = response.data["slug"]

        self.client.post(self.SIGN_UP_URL, self.user_cred1, format="json")
        rater_login_response = self.client.post(
            reverse("authentication:user_login"), self.user_cred1, format="json"
        )

        rater_token = rater_login_response.data["token"]

        rate = {"rate": {"rating": "5", "note": "I loved the dragons story"}}

        response = self.rate_article(rater_token, slug, rate)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_can_rate_article_rate_value_greater_than_5(self):
        """
        Tests whether a user can rate an article with a value greater than 5
        """

        self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
        login_response = self.client.post(
            reverse("authentication:user_login"), self.user_cred, format="json"
        )
        author_token = login_response.data["token"]

        response = self.create_article(author_token, self.testArticle)
        slug = response.data["slug"]

        self.client.post(self.SIGN_UP_URL, self.user_cred1, format="json")
        rater_login_response = self.client.post(
            reverse("authentication:user_login"), self.user_cred1, format="json"
        )

        rater_token = rater_login_response.data["token"]
        rate = {"rate": {"rating": 6, "note": "I loved the dragons story"}}

        response = self.rate_article(rater_token, slug, rate)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_can_rate_article_rate_value_less_than_1(self):
        """Tests whether a user can rate an article with a value less than 1"""

        self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
        login_response = self.client.post(
            reverse("authentication:user_login"), self.user_cred, format="json"
        )
        author_token = login_response.data["token"]
        response = self.create_article(author_token, self.testArticle)

        slug = response.data["slug"]

        self.client.post(self.SIGN_UP_URL, self.user_cred1, format="json")
        rater_login_response = self.client.post(
            reverse("authentication:user_login"), self.user_cred1, format="json"
        )

        rater_token = rater_login_response.data["token"]

        rate = {"rate": {"rating": 0, "note": "I loved the dragons story"}}

        response = self.rate_article(rater_token, slug, rate)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)
