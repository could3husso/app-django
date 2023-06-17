from django.http import Http404

from articles.models import Article
from articles.serializers import ArticleSerializer

class ArticleRepository():

    def __get_article_by(self, article_id):
        try:
            return Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise Http404

    def fetch_one(self, article_id) -> ArticleSerializer:
        article = self.__get_article_by(article_id)
        return ArticleSerializer(article)

    def fetch_all(self) -> ArticleSerializer :
        articles = Article.objects.all()
        return ArticleSerializer(articles, many=True).data

    def delete_article(self, article_id):
        article = self.__get_article_by(article_id)
        article.delete()

    def set_article(self, payload, article_id=None):

        if article_id is None:
            article_serializer = ArticleSerializer(data=payload)
        else:
            article = self.__get_article_by(article_id)
            article_serializer = ArticleSerializer(article, data=payload)

        if article_serializer.is_valid():

            article_serializer.save() 
            return {'data': article_serializer.data}
        
        return {'errors': article_serializer.errors}
    