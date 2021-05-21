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
    path(
        "<str:slug>/", ArticleViewSet.as_view({"get": "retrieve"}), name="fetch_article"
    ),
    path(
        "<str:slug>/", ArticleViewSet.as_view({"put": "update"}), name="update_article"
    ),
    path(
        "<str:slug>/",
        ArticleViewSet.as_view({"delete": "destroy"}),
        name="delete_article",
    ),
    
    path("<str:slug>/like/", LikeAPIView.as_view(), name="like_article"),
    path(
        "<str:slug>/dislike/", DisLikeAPIView.as_view(), name="dislike_article"
    ),
    path(
        "<str:slug>/bookmark/",
        BookmarkAPIView.as_view(),
        name="bookmark_article",
    ),
    
    path("search", ArticleSearchList.as_view(), name="search"),
    
    path("<str:article_slug>/favorite/", ArticlesFavoriteAPIView.as_view()),
    path(
        "<slug>/comments",
        CommentsListCreateAPIView.as_view(),
        name="comment_article",
    ),
    path("<slug>/comments/<pk>", CommentRetrieveUpdateDestroy.as_view()),
    path("<slug>/comments/<pk>/like", LikeComment.as_view()),
    path("<slug>/comments/<pk>/dislike", DislikeComment.as_view()),
    path("<slug>/rate/", RateArticlesAPIView.as_view()),
    path("<slug>/report", ReportCreateAPIView.as_view()),
    path("<slug>/reports", ReportListAPIView.as_view()),
]
