from django.urls import path, include

from api_v2.views import ArticleView, ArticleDetailUpdateDeleteView


app_name = 'api_v2'


article_urls = [
    path('', ArticleView.as_view(), name='articles'),
    path('<int:pk>/', ArticleDetailUpdateDeleteView.as_view(), name='update_article'),
]


urlpatterns = [
    path('articles/', include(article_urls)),
]
