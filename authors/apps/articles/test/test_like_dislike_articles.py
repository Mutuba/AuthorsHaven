# from django.urls import reverse
# from rest_framework.views import status
# from authors.apps.base_test import BaseTest


# class DislikeLikeArticleTestCase(BaseTest):
#     """Tests Like and Dislike articles views"""
#     def test_if_user_cannot_like_article_without_authentication(self):
#         """Test if user cannot like article without authentication"""
#         response = self.client.put(path="/api/articles/how-to-feed-your-dragon/like")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(
#             response.data["detail"], "Authentication credentials were not provided."
#         )

#     def test_if_user_can_dislike_without_authentication(self):
#         """Test if user can dislike article without authentication"""
#         response = self.client.put(path="/api/articles/how-to-feed-your-dragon/dislike")

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(
#             response.data["detail"], "Authentication credentials were not provided."
#         )

#     def test_if_user_can_like_unexisting_article(self):
#         """Test if the user can like an article that does not exist"""
#         token = self.get_token()
#         response = self.client.put(
#             path="/api/articles/how-to-train-your-dragon/like",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["message"], "The article does not exist.")

#     def test_if_user_can_dislike_unexisting_article(self):
#         """Test if the user can like an article that does not exist"""

#         token = self.get_token()
#         response = self.client.put(
#             path="/api/articles/how-to-train-your-dragon/dislike",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["message"], "The article does not exist.")

#     def test_if_user_liking_is_successful(self):
#         """Test if user liking is successful, if like does not exist"""
#         token = self.get_token()
#         self.create_article(token, self.testArticle)
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/like",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "Added to Liked articles")

#     def test_successful_article_disliking(self):
#         """Test a successful disliking of an article"""
#         token = self.get_token()
#         self.create_article(token, self.testArticle)
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/dislike",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "You Dislike this Article")

#     def test_response_of_adding_a_like_after_adding_a_dislike(self):
#         """Test the response of adding a like after adding a dislike"""
#         token = self.get_token()
#         self.create_article(token, self.testArticle)
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/dislike",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "You Dislike this Article")
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/like",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(
#             response.data["message"], "Removed from dislike and Added to Liked articles"
#         )

#     def test_response_of_adding_a_dislike_after_adding_a_like(self):
#         """Test the response of adding a dislike after adding a like"""
#         token = self.get_token()
#         self.create_article(token, self.testArticle)
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/like",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "Added to Liked articles")
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/dislike",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(
#             response.data["message"],
#             "Removed from Liked Articles and Added to Disliked articles",
#         )

#     def test_response_of_double_liking(self):
#         """Test the response of liking an article twice"""
#         token = self.get_token()
#         self.create_article(token, self.testArticle)
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/like",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "Added to Liked articles")
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/like",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "You no longer like this article")

#     def test_response_of_double_disliking(self):
#         """Test the response of disliking an article twice"""
#         token = self.get_token()
#         self.create_article(token, self.testArticle)
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/dislike",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "You Dislike this Article")
#         response = self.client.put(
#             path="/api/articles/how-to-feed-your-dragon/dislike",
#             HTTP_AUTHORIZATION="Bearer " + token,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "You no longer dislike this article")
