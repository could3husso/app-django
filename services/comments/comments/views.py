from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view

from comments.core import comment_repository

@api_view(['GET', 'POST'])
def comments(request):
    """
    List all post, or create a new one.
    """
    if request.method == 'GET':
        comments = comment_repository.fetch_all()
        return JsonResponse(comments, safe=False)

    elif request.method == 'POST':
        paylaod = comment_repository.set_article(payload=request.data)
        if 'data' in paylaod:
            return Response(paylaod['data'], status=status.HTTP_201_CREATED)
        return Response(paylaod['errors'], status=status.HTTP_400_BAD_REQUEST)

class CommentList(APIView):
    """
    List all comments, or add a new comments.
    """
    def get(self, request, pk, format=None):
        serializer = comment_repository.fetch_one(pk)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        paylaod =  comment_repository.set_article(request.data, comment_id=pk)
        if 'data' in paylaod:
            return Response(paylaod['data'])
        return Response(paylaod['errors'], status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment_repository.delete_comment(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)