from rest_framework import routers
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    ArticleViewSet,
    LikeAPIView,
    DisLikeAPIView,
    ArticleSearchList,
    ArticlesFavoriteAPIView,
    CommentsListCreateAPIView,
    CommentRetrieveUpdateDestroy,
    LikeComment,
    DislikeComment,
    RateArticlesAPIView,
    BookmarkAPIView,
    ReportCreateAPIView,
    ReportListAPIView,
)

router = DefaultRouter(trailing_slash=False)


app_name = "articles"

urlpatterns = [
    path("", ArticleViewSet.as_view({"get": "list"}), name="fetch_articles"),
    path("articles/<str:slug>/like/", LikeAPIView.as_view(), name="like_article"),
    path(
        "articles/<str:slug>/dislike/", DisLikeAPIView.as_view(), name="dislike_article"
    ),
    path(
        "articles/<str:slug>/bookmark/",
        BookmarkAPIView.as_view(),
        name="bookmark_article",
    ),
    path("search/articles", ArticleSearchList.as_view(), name="search"),
    path("articles/<str:article_slug>/favorite/", ArticlesFavoriteAPIView.as_view()),
    path(
        "articles/<slug>/comments",
        CommentsListCreateAPIView.as_view(),
        name="comment_article",
    ),
    path("articles/<slug>/comments/<pk>", CommentRetrieveUpdateDestroy.as_view()),
    path("articles/<slug>/comments/<pk>/like", LikeComment.as_view()),
    path("articles/<slug>/comments/<pk>/dislike", DislikeComment.as_view()),
    path("articles/<slug>/rate/", RateArticlesAPIView.as_view()),
    path("articles/<slug>/report", ReportCreateAPIView.as_view()),
    path("articles/<slug>/reports", ReportListAPIView.as_view()),
]
