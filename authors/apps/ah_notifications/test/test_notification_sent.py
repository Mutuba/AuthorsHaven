"""
Notification tests
"""
from authors.apps.base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status


class NotificationTestCase(BaseTest):
    """
    notifications tests
    """

    comment = {"comment": {"body": "I do believe"}}

    def test_notification_sent_after_article_creation(self):
        """
        Test that a notification is sent to users after an articel is created

        User2 starts to follow User1, then User1 creates an article.

        Expected behaviour: User2 should get a notification that User1 has created an article

        """
        mutuba_token = self.get_mutuba_token()
        jason_token = self.get_jason_token()
        res = self.client.put(
            "/api/profiles/Mutuba/follow",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
        )

        resp = self.client.get(
            "/api/profiles/Mutuba/followers",
            HTTP_AUTHORIZATION="Bearer " + mutuba_token,
            format="json",
        )

        self.create_article(mutuba_token, self.testArticle)

        response = self.client.get(
            "/api/notifications",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_get_single_notification(self):
        mutuba_token = self.get_mutuba_token()
        jason_token = self.get_jason_token()
        res = self.client.put(
            "/api/profiles/Mutuba/follow",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
            format="json",
        )

        resp = self.client.get(
            "/api/profiles/Mutuba/followers",
            HTTP_AUTHORIZATION="Bearer " + mutuba_token,
            format="json",
        )

        self.create_article(mutuba_token, self.testArticle)

        response = self.client.get(
            "/api/notifications/1",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_notification_not_sent_to_non_followers(self):
        """
        test notifications for article creation should only be sent to followers

        """
        mutuba_token = self.get_mutuba_token()
        jason_token = self.get_jason_token()
        mercy_token = self.get_mercy_token()
        res = self.client.put(
            "/api/profiles/Mutuba/follow",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
            format="json",
        )

        resp = self.client.get(
            "/api/profiles/Mutuba/followers",
            HTTP_AUTHORIZATION="Bearer " + mutuba_token,
            format="json",
        )

        self.create_article(mutuba_token, self.testArticle)

        response = self.client.get(
            "/api/notifications",
            HTTP_AUTHORIZATION="Bearer " + mercy_token,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)

    def test_notification_sent_after_comment(self):
        """
        Test notitification sent after article is favorited
        """
        mutuba_token = self.get_mutuba_token()
        jason_token = self.get_jason_token()
        mercy_token = self.get_mercy_token()

        response = self.create_article(mutuba_token, self.testArticle)

        slug = response.data["slug"]
        self.client.post(
            "/api/articles/" + slug + "/favorite",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
            format="json",
        )
        res = self.client.post(
            "/api/articles/" + slug + "/comments",
            self.comment,
            HTTP_AUTHORIZATION="Bearer " + mercy_token,
            format="json",
        )
        response = self.client.get(
            "/api/notifications",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_notification_sent_only_to_users_who_favorited_the_article(self):
        """
        notifications should only be sent to users who favorited the article
        """
        mutuba_token = self.get_mutuba_token()
        jason_token = self.get_jason_token()
        mercy_token = self.get_mercy_token()
        loice_token = self.get_loice_token()
        response = self.create_article(mutuba_token, self.testArticle)
        slug = response.data.get("slug")
        self.client.post(
            "/api/articles/" + slug + "/favorite",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
            format="json",
        )
        res = self.client.post(
            "/api/articles/" + slug + "/comments",
            self.comment,
            HTTP_AUTHORIZATION="Bearer " + mercy_token,
            format="json",
        )
        response = self.client.get(
            "/api/notifications",
            HTTP_AUTHORIZATION="Bearer " + loice_token,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)

    def test_notification_not_sent_to_unsubscribed_users(self):
        """
        notifications should only be sent to subscribed users
        """
        mutuba_token = self.get_mutuba_token()
        jason_token = self.get_jason_token()
        mercy_token = self.get_mercy_token()

        response = self.create_article(mutuba_token, self.testArticle)
        slug = response.data.get("slug")

        self.client.post(
            "/api/articles/" + slug + "/favorite",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
            format="json",
        )
        self.client.put(
            "/api/notifications/unsubscribe",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
            format="json",
        )
        res = self.client.post(
            "/api/articles/" + slug + "/comments",
            self.comment,
            HTTP_AUTHORIZATION="Bearer " + mercy_token,
            format="json",
        )
        response = self.client.get(
            "/api/notifications",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)

    def test_user_can_subscribe_and_unsubscribe(self):
        """
        users should be able to subscribe and unsubscribe to notifications
        """
        mutuba_token = self.get_mutuba_token()
        jason_token = self.get_jason_token()
        mercy_token = self.get_mercy_token()

        response = self.create_article(mutuba_token, self.testArticle)
        slug = response.data.get("slug")

        self.client.post(
            "/api/articles/" + slug + "/favorite",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
            format="json",
        )
        self.client.put(
            "/api/notifications/unsubscribe",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
            format="json",
        )
        res = self.client.post(
            "/api/articles/" + slug + "/comments",
            self.comment,
            HTTP_AUTHORIZATION="Bearer " + mercy_token,
            format="json",
        )
        response = self.client.get(
            "/api/notifications",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)
        self.client.put(
            "/api/notifications/subscribe",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
            format="json",
        )
        res = self.client.post(
            "/api/articles/" + slug + "/comments",
            self.comment,
            HTTP_AUTHORIZATION="Bearer " + mercy_token,
            format="json",
        )
        response = self.client.get(
            "/api/notifications",
            HTTP_AUTHORIZATION="Bearer " + jason_token,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)
