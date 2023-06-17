from django.http import Http404

from comments.models import Comment
from comments.serializers import CommentSerializer

class CommentsRepository():
     
    def __get_comment_by(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise Http404

    def fetch_one(self, comment_id) -> CommentSerializer:
        article = self.__get_comment_by(comment_id)
        return CommentSerializer(article)
    
    def fetch_all(self) -> CommentSerializer :
        comments = Comment.objects.all()
        return CommentSerializer(comments, many=True).data

    def delete_comment(self, comment_id):
        comment = self.__get_comment_by(comment_id)
        comment.delete()

    def set_comment(self, payload, comment_id=None):

        if comment_id is None:
            article_serializer = CommentSerializer(data=payload)
        else:
            comment = self.__get_comment_by(comment_id)
            comment_serializer = CommentSerializer(comment, data=payload)

        if comment_serializer.is_valid():

            comment_serializer.save() 
            return {'data': comment_serializer.data}
        
        return {'errors': comment_serializer.errors}

