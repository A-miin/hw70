import json

from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from article.models import Article
from api_v2.serializers import ArticleSerializer


class ArticleView(APIView):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        response_data = serializer.data

        return Response(data=response_data)

    def post(self, request, *args, **kwargs):
        article_data = request.data
        serializer = ArticleSerializer(data=article_data)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        return JsonResponse({'id': article.id})


class ArticleDetailUpdateDeleteView(APIView):
    def put(self, request, *args, **kwargs):
        article_id = self.kwargs.get('pk', 0)
        instance = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


