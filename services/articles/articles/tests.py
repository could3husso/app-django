from django.test import TestCase
from rest_framework.test import RequestsClient
from django.urls import include, path, reverse
from rest_framework import status


# Create your tests here.
from .models import Article
from articles.core import article_repository

class ArticleReposTestCase(TestCase):
    
    def test_create_an_article(self):
        payload = {'title': 'test_create_an_article', 'body': 'create_an_article'}
        created = article_repository.set_article(payload)

        expected_article = Article.objects.get(body=payload['body'])
        self.assertEqual(expected_article.title, created['data']['title'])

    def test_update_an_article(self):

        payload = {'title': 'test_update_an_article', 'body': 'update an article'}
        article = article_repository.set_article(payload)
        # expected_article = Article.objects.get(title=payload['title'])

        data = {'title': 'update_an_article', 'body': 'update an article'}
        update = article_repository.set_article(data, article['data']['id'])

        expected_article = Article.objects.get(title=data['title'])
        self.assertNotEqual(expected_article.title, payload['title'])

    def test_delete_an_article(self):

        with self.assertRaises(Article.DoesNotExist) as context:

            payload = {'title': 'test_delete_an_article', 'body': 'delete an article'}
            article = article_repository.set_article(payload)
            article_supprime = article_repository.delete_article(article['data']['id'])

            expected_article = Article.objects.get(title=payload['title'])

            self.assertRaises(Article.DoesNotExist, expected_article)
        

class ReauestClientTestCase(TestCase):

    def setUp(self):
        client = RequestsClient()

        payload = {'title': 'test_request', 'body': 'fetch one article'}
        article = article_repository.set_article(payload)

        payload = {'title': 'request one client', 'body': 'class is useful if you want to write tests that solely interact with the service interface'}
        article = article_repository.set_article(payload)

    def test_fecth_one(self):
        payload = {'title': 'ModelSerializer', 'body': 'e can actually also save ourselves some time by using the ModelSerializer'}
        article = article_repository.set_article(payload)

        id = article['data']['id']

        url = f'http://127.0.0.1:8000/articles/{id}/'
        response = self.client.get(url, format='json')
        self.assertIsNotNone(response.data)


    def test_fecth_all(self):
        
        response = self.client.get('http://127.0.0.1:8000/articles/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    
