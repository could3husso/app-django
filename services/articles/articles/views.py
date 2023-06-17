from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view

from articles.core import article_repository


@api_view(['GET'])
def healt_check(request):
    pass

@api_view(['GET', 'POST'])
def articles(request):
    """
    List all post, or create a new one.
    """
    if request.method == 'GET':
        articles = article_repository.fetch_all()
        return JsonResponse(articles, safe=False)

    elif request.method == 'POST':
        paylaod = article_repository.set_article(payload=request.data)
        if 'data' in paylaod:
            return Response(paylaod['data'], status=status.HTTP_201_CREATED)
        return Response(paylaod['errors'], status=status.HTTP_400_BAD_REQUEST)

class ArticleDetail(APIView):
    """
    Retrieve, update or delete article instance.
    """
    
    def get(self, request, pk, format=None):
        serializer = article_repository.fetch_one(pk)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        paylaod =  article_repository.set_article(request.data, article_id=pk)
        if 'data' in paylaod:
            return Response(paylaod['data'])
        return Response(paylaod['errors'], status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article_repository.delete_article(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)