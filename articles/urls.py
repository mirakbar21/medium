from django.urls import path, include
from .import views
from comments import views as comments_views

urlpatterns = [
    path('', views.IndexView.as_view(), name = "articles"),
    path('<int:pk>', views.ArticleDetailView.as_view(), name = "article_details"),
    path('create_article', views.CreateArticle.as_view(), name = 'create_article'),
    path('<int:pk>/edit', views.EditArticle.as_view(), name = 'edit_article'),
    path('<int:pk>/delete', views.DeleteArticle.as_view(), name = 'confirm_delete'),
    path('<int:article_id>/applaud/', views.article_applaud, name='article_applaud'),
    path('<int:article_id>/comment', comments_views.add_comment, name = 'add_comment'),
    path('search/', views.query, name='search_results'),
]