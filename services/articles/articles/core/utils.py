from rest_framework.views import exception_handler
from kombu import Producer, Queue, Exchange
from kombu import Connection

from messaging import PayloadConsumer


queue = Queue('api_responses', Exchange('api_gateway', type='direct'))

BROKER_URI = 'amqp://guest:guest@127.0.0.1:5672//'

def custom_exception_handler(exec, context):

    response = exception_handler(exec, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response

def article_consumer():
    
    with Connection(BROKER_URI) as conn:
        worker = PayloadConsumer(Connection, 'articles', 'articles')
        worker.run()



