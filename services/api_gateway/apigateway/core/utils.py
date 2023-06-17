from kombu import Producer, Queue, Exchange, Connection
from kombu.mixins import ConsumerMixin

queue = Queue('api_responses', Exchange('api_gateway', type='direct'))

BROKER_URI = 'amqp://guest:guest@127.0.0.1:5672//'

class PayloadConsumer(ConsumerMixin):

    def __init__(self, connection):
        
        self.connection = connection

    def get_consumers(self, Consumer, channel):

        return [
            Consumer(queues=queue, on_message=self.on_request,
            accept={'application/json'}, prefetch_count=1,)
        ]
    
    def process_task(self, body, message):

        message.ack()

def set_payload(action, message):
    return {'action': action, 'payload': message}

def payload_publisher(queue_name, routing_key, payload, 
                      exchange_name='backend-service'):

    task_queue = Queue(queue_name, Exchange(exchange_name, type='direct'), 
                       routing_key=routing_key)

    with Connection(BROKER_URI) as conn:
        with conn.channel() as channel:
            producer = Producer(channel)
            producer.publish(
                payload, retry=True, exchange=task_queue.exchange,
                routing_key=task_queue.routing_key,
                declare=[task_queue], # declares exchange, queue and binds.
            )
