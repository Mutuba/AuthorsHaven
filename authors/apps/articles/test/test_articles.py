# from authors.apps.base_test import BaseTest
# from django.urls import reverse
# from rest_framework.views import status
# import json


# class ArticleTestCase(BaseTest):
#     """
#     Class implements tests for artcles
#     """
#     def test_create_successfully(self):
#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]

#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }

#         response = self.create_article(token, article)

#         self.assertEquals(status.HTTP_201_CREATED, response.status_code)

#     def test_create_article_with_fake_token(self):
#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = "hgbbbjbhhjknkj"

#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }

#         response = self.create_article(token, article)

#         self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)

#     def test_create_article_with_empty_data(self):
#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]

#         article = {
#             "article": {
#                 "title": "",
#                 "description": "",
#                 "body": "",
#             }
#         }

#         response = self.create_article(token, article)
#         self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

#     def test_user_can_get_articles(self):
#         """
#         Tests that user can get a list of articles

#         """
#         self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]

#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }

#         self.create_article(token, article)
#         response = self.client.get("/api/articles/list")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_any_user_can_get_paginated_articles(self):
#         """
#         Test user can view paginated data
#         """
#         # Signs up User
#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         # Signs in User
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         article = self.testArticle
#         # runs create article 21 times so as to create multiple articles
#         for i in range(0, 21):
#             response = self.create_article(token, article)
#         else:
#             pass

#         response = self.client.get("/api/articles/list")
#         self.assertEquals(response.data["count"], 21)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_unauthenticated_user_cannot_create_article(self):
#         """
#         Test that a user without an account cannot create an article
#         """
#         response = self.client.post(
#             self.SIGN_UP_URL, self.user_cred_wrong_pass, format="json"
#         )
#         response = self.client.post(
#             reverse("authentication:user_login"),
#             self.user_cred_wrong_pass,
#             format="json",
#         )
#         # fake token because user is not verified
#         token = "gv jkknk m lk"

#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }

#         response = self.create_article(token, article)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_update_article_successfully(self):
#         """Tests whether a user can update an article
#         Method registers a user, logs in the user,
#         creates an article, then updates the article

#         """

#         self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         response = self.create_article(token, self.testArticle)

#         self.assertEquals(status.HTTP_201_CREATED, response.status_code)

#         # Update the created article
#         response = self.update_article(
#             token, "how-to-feed-your-dragon", self.testArticle1
#         )

#         self.assertIn("how-to-train-your-dragon", response.content.decode())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_delete_article_successfully(self):
#         """
#         Tests whether a user can update an article
#         Method registers a user, logs in the user,
#         creates an article, then updates the article

#         """

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         response = self.create_article(token, self.testArticle)
#         self.assertEquals(status.HTTP_201_CREATED, response.status_code)
#         # Update the created article
#         response = self.delete_article(token, "how-to-feed-your-dragon")
#         response = self.client.get("/api/articles/how-to-feed-your-dragon")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_user_cannot_delete_article_when_not_article_author(self):
#         """
#         Tests whether a user can delete an article when not the author
#         Method registers a user, logs in the user,
#         creates an article, then updates the article

#         """

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]

#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }

#         response = self.create_article(token, article)
#         # Asserr true that an article has been created
#         self.assertEquals(status.HTTP_201_CREATED, response.status_code)

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred1, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred1, format="json"
#         )

#         token = response.data["token"]
#         # Delete the article created by another user.
#         # Expects to throw a 404 error
#         response = self.delete_article(token, "how-to-feed-your-dragon")

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_user_cannot_update_an_article_when_not_article_author(self):
#         """
#         Tests whether a user can update an article when not author
#         Method registers a user, logs in the user,
#         creates an article, then logs in another,
#         and tries to update the article

#         """

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]

#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }

#         response = self.create_article(token, article)
#         # Assert true that an article has been created
#         self.assertEquals(status.HTTP_201_CREATED, response.status_code)

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred1, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred1, format="json"
#         )
#         tokenn = response.data["token"]
#         # Update the article created by another user.
#         # Expect a 404 error
#         response = self.update_article(
#             tokenn, "how-to-feed-your-dragon", self.testArticle1
#         )

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_user_gets_404_not_found_when_updating_an_article_not_found(self):
#         """
#         Tests whether a user cannot update an article when the slug param is non-existent
#         Method registers a user, logs in the user,
#         and tries to update an article using non existent slug

#         """

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]

#         # Update the article by passing a non existent slug
#         # Expect to throw a 404 error
#         response = self.update_article(
#             token, "how-to-feed-your-dragonn", self.testArticle1
#         )

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_user_gets_404_not_found_when_deleting_article_not_found(self):
#         """
#         Tests whether a user cannot delete an article when slug param is non-existent
#         Method registers a user, logs in the user,
#         and tries to delete an article by passing a non-existent slug

#         """

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]

#         # Expects to throw a 404 error

#         response = self.delete_article(token, "how-to-feed-your-dragonn")

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_user_gets_404_not_found_when_deleting_an_article_already_deleted(self):
#         """
#         Tests whether a user cannot delete an article when already deleted
#         Method registers a user, logs in the user,
#         creates an article, then deletes,
#         and tries to delete the article again

#         """

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]

#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }

#         response = self.create_article(token, article)
#         # Assert true that an article has been created
#         self.assertEquals(status.HTTP_201_CREATED, response.status_code)

#         # Delete the article created by another user.
#         # Expects success 200 OK
#         response = self.delete_article(token, "how-to-feed-your-dragon")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Try to delete an already deleted article, expects a 404_NOT_FOUND

#         response = self.delete_article(token, "how-to-feed-your-dragon")

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_unauthenticated_user_cannot_favorite_article(self):
#         """
#         Tests whether a user who is unauthenticated cant' favorite an article

#         """
#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }
#         response = self.create_article(token, article)
#         token = ""
#         response = self.favorite_article(token, "how-to-feed-your-dragon")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_unauthenticated_user_cannot_unfavorite_article(self):
#         """
#         Tests whether a user who is unauthenticated cant' unfavorite an article
#         """
#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }
#         response = self.create_article(token, article)

#     def test_favorite_non_existent_article(self):
#         """
#         Tests whether a user  cant favorite a non-existent article
#         """
#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         response = self.favorite_article(token, "non-existent-slug")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_unfavorite_non_existent_article(self):
#         """
#         Tests whether a user cant unfavorite a non-existent article

#         """
#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         response = self.unfavorite_article(token, "non-existent-slug")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_user_can_favorite_article(self):
#         """Tests whether a user can favorite an article"""

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }

#         response = self.create_article(token, article)

#         # favorite the article
#         # Expects success 200 OK
#         response = self.favorite_article(token, "how-to-feed-your-dragon")
#         self.assertTrue(response.data["favorited"])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user_can_unfavorite_article(self):
#         """Tests whether a user can ufavorite an article"""

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }

#         response = self.create_article(token, article)

#         # unfavorite the article
#         # Expects success 200 OK
#         response = self.unfavorite_article(token, "how-to-feed-your-dragon")
#         self.assertFalse(response.data["favorited"])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_articles_are_unfavorited(self):
#         """
#         Tests whether a all articles are ufavorited if a user retrives all
#         articles without being authenticated

#         """

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }
#         response = self.create_article(token, article)

#         response = self.client.get("/api/articles/list")
#         # tests if the favorited field in results is False
#         self.assertFalse(response.data["results"][0]["favorited"])

#     def test_articles_are_favorited(self):
#         """
#         Tests whether a all articles are favorited if a user retrives all
#         articles after being authenticated
#         """

#         response = self.client.post(self.SIGN_UP_URL, self.user_cred, format="json")
#         response = self.client.post(
#             reverse("authentication:user_login"), self.user_cred, format="json"
#         )
#         token = response.data["token"]
#         article = {
#             "article": {
#                 "title": "How to feed your dragon",
#                 "description": "Wanna know how?",
#                 "body": "You don't believe?",
#             }
#         }
#         response = self.create_article(token, article)
#         response = self.favorite_article(token, "how-to-feed-your-dragon")
#         response = self.get_articles(token)
#         # tests if the favorited field in results is True after authentication
#         self.assertTrue(response.data["results"][0]["favorited"])
