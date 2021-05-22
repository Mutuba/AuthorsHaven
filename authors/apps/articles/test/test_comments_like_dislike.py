from authors.apps.base_test import BaseTest
from django.urls import reverse
from authors.apps.articles.models import Article
from rest_framework.views import status
import json


class CommentsLikeDislikeTestCase(BaseTest):
    """
    Class implements tests for liking and disliking comments.
    """

    comment = {"comment": {"body": "Wagwan"}}

    def test_like_comment(self):
        """Test test the liking of a comment"""
        # created a user, logged in the user
        # Created a token
        token = self.get_token()

        # created the article
        self.create_article(token, self.testArticle)
        # creating a comment
        response = self.create_comment(self.comment)
        comment_id = response.data["id"]
        # like a comment
        response = self.client.put(
            "/api/articles/how-to-feed-your-dragon/comments/"
            + str(comment_id)
            + "/like",
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_dislike_comment(self):
        """Test test the liking of a comment"""
        token = self.get_token()

        # created the article
        self.create_article(token, self.testArticle)
        # creating a comment
        response = self.create_comment(self.comment)
        comment_id = response.data["id"]
        # like a comment
        response = self.client.put(
            "/api/articles/how-to-feed-your-dragon/comments/"
            + str(comment_id)
            + "/dislike",
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_like_missing_article(self):
        """Test test the liking of a comment"""
        token = self.get_token()

        self.create_article(token, self.testArticle)
        response = self.create_comment(self.comment)

        comment_id = response.data["id"]

        response = self.client.put(
            "/api/articles/how-to-feed-your-drago/comments"
            + str(comment_id)
            + "/dislike",
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_like_missing_comment(self):
        """Test test the liking of a comment"""
        token = self.get_token()

        self.create_article(token, self.testArticle)

        response = self.client.put(
            "/api/articles/how-to-feed-your-dragon/comments/99/dislike",
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
