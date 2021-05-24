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
    path("", ArticleViewSet.as_view({"post": "create"}), name="create_article"),
    path("list", ArticleViewSet.as_view({"get": "list"}), name="fetch_articles"),
    path("search", ArticleSearchList.as_view(), name="search"),
    path(
        "<slug:slug>",
        ArticleViewSet.as_view({"get": "retrieve"}),
        name="fetch_article",
    ),
    path(
        "<slug:slug>/update",
        ArticleViewSet.as_view({"put": "update"}),
        name="update_article",
    ),
    path(
        "<slug:slug>/delete",
        ArticleViewSet.as_view({"delete": "destroy"}),
        name="delete_article",
    ),
    path("<slug:slug>/like", LikeAPIView.as_view(), name="like_article"),
    path("<slug:slug>/dislike", DisLikeAPIView.as_view(), name="dislike_article"),
    path(
        "<slug:slug>/bookmark",
        BookmarkAPIView.as_view(),
        name="bookmark_article",
    ),
    path("<slug:article_slug>/favorite", ArticlesFavoriteAPIView.as_view()),
    path(
        "<slug:slug>/comments",
        CommentsListCreateAPIView.as_view(),
        name="comment_article",
    ),
    path("<slug:slug>/comments/<int:pk>", CommentRetrieveUpdateDestroy.as_view()),
    path("<slug:slug>/comments/<int:pk>/like", LikeComment.as_view()),
    path("<slug:slug>/comments/<int:pk>/dislike", DislikeComment.as_view()),
    path("<slug:slug>/rate", RateArticlesAPIView.as_view()),
    path("<slug:slug>/report", ReportCreateAPIView.as_view()),
    path("<slug:slug>/reports", ReportListAPIView.as_view()),
]
