from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apigateway.core.utils import payload_publisher

# Create your views here.
@api_view(['GET', 'POST'])
def posts(request, action):
    if request.method == 'GET':
        return Response("You're looking at question")
    
    message = {'data': request.data, 'action': action}
    payload_publisher('articles_queue', 'articles', message)

    return Response("", status=status.HTTP_201_CREATED)

@api_view(['POST'])
def comments(request, action):
    
    message = {'data': request.data, 'action': action}
    payload_publisher('comments_queue', 'comments', message)

    return Response("", status=status.HTTP_201_CREATED)

