"""
Comments tests
"""
from authors.apps.base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status
import json


class CommentTestCase(BaseTest):
    """
    Comment Test Class, Inherits from Basetest
    """

    comment = {"comment": {"body": "I do believe"}}
    empty_comment = {"comment": {"body": " "}}

    def test_add_comments(self):
        self.create_article(self.get_token(), self.testArticle)
        response = self.create_comment(self.comment)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_comment_on_non_existent_article(self):
        """
        test that it throws a 404 error
        """
        token = self.get_token()
        response = self.client.post(
            "/api/articles/not-found/comments",
            self.comment,
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_empty_comment(self):
        """
        Test it throws 400 error if comment body is empty
        """
        self.create_article(self.get_token(), self.testArticle)
        response = self.create_comment(self.empty_comment)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_comments(self):
        """
        test user can get all comments to an article
        """
        self.create_article(self.get_token(), self.testArticle)
        self.create_comment(self.comment)
        response = self.client.get("/api/articles/how-to-feed-your-dragon/comments")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comments_for_non_existant_article(self):
        response = self.client.get("/api/articles/test-article-wrong/comments")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_comments(self):
        """
        test that user can get single comment
        """
        self.create_article(self.get_token(), self.testArticle)
        response = self.create_comment(self.comment)
        article_id = response.data["id"]
        response = self.client.get(
            "/api/articles/how-to-feed-your-dragon/comments/" + str(article_id)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existent_comment(self):
        """
        test that throws 404 error if comment does not exist
        """
        self.create_article(self.get_token(), self.testArticle)
        response = self.client.get("/api/articles/how-to-feed-your-dragon/comments/500")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_wrong_id(self):
        """
        test that user can delete comment
        """
        token = self.get_token()

        self.create_article(token, self.testArticle)
        response = self.client.delete(
            "/api/articles/how-to-feed-your-dragon/comments/1",
            HTTP_AUTHORIZATION="Bearer " + token,
        )
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_comment_with_correct_id(self):
        """
        Test that user can delete comment with right id
        """
        token = self.get_token()
        self.create_article(token, self.testArticle)

        response = self.create_comment(self.comment)

        article_id = response.data["id"]
        response = self.client.delete(
            "/api/articles/how-to-feed-your-dragon/comments/" + str(article_id),
            HTTP_AUTHORIZATION="Bearer " + token,
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_non_owner_cannot_delete_article(self):
        """
        Test that user can only delete their comments
        """
        token = self.get_token()
        token2 = self.get_user2_token()
        self.create_article(token, self.testArticle)
        response = self.create_comment(self.comment)

        article_id = response.data["id"]
        response = self.client.delete(
            "/api/articles/how-to-feed-your-dragon/comments/" + str(article_id),
            HTTP_AUTHORIZATION="Bearer " + token2,
        )
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)
