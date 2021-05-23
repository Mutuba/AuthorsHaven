from authors.apps.base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status


class ReportArticleTestCase(BaseTest):
    def test_if_user_can_report_without_authentication(self):
        """Test if user can report an article without authentication"""
        response = self.client.put(path="/api/articles/how-to-feed-your-dragon/report")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_if_none_admin_user_can_get_reports(self):
        token = self.get_token()
        self.create_article(token, self.testArticle)
        response = self.client.get(
            path="/api/articles/how-to-feed-your-dragon/reports",
            HTTP_AUTHORIZATION="Bearer " + token,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_user_can_report_articles(self):
        token = self.get_token()
        self.create_article(token, self.testArticle)
        data = {"report": {"body": "A lot of plagiarism"}}
        response = self.client.post(
            path="/api/articles/how-to-feed-your-dragon/report",
            data=data,
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_user_can_report_articles_without_body(self):
        token = self.get_token()
        self.create_article(token, self.testArticle)
        response = self.client.post(
            path="/api/articles/how-to-feed-your-dragon/report",
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_user_can_report_missing_article(self):
        token = self.get_token()
        response = self.client.post(
            path="/api/articles/how-toc-your-dragon/report",
            HTTP_AUTHORIZATION="Bearer " + token,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(
            response.data["detail"], "An article with that slug does not exist"
        )

    def test_if_admin_can_list_reports(self):
        token = self.get_token()
        self.create_article(token, self.testArticle)

        data = {"report": {"body": "A lot of plagiarism"}}
        response = self.client.post(
            path="/api/articles/how-to-feed-your-dragon/report",
            data=data,
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.login_admin()
        token = response.data["token"]
        response = self.client.get(
            path="/api/articles/how-to-feed-your-dragon/reports",
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_if_admin_can_list_reports_of_non_existing_article(self):
        response = self.login_admin()
        token = response.data["token"]
        response = self.client.get(
            path="/api/articles/how-to-feed-your-dragon/reports",
            HTTP_AUTHORIZATION="Bearer " + token,
            format="json",
        )
        self.assertEqual(
            response.data["detail"], "An article with this slug does not exist."
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
