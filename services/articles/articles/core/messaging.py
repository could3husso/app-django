from kombu import Producer, Queue, Exchange
from kombu.mixins import ConsumerProducerMixin, ConsumerMixin
from kombu import Connection, Consumer, Queue


class PayloadConsumer(ConsumerMixin):

    def __init__(self, connection , queue_name, 
                 routing_key,  exhange_type='direct', exchange_name="backend"):
        
        self.connection = connection
        self.task_queue = Queue(queue_name, 
                           Exchange(exchange_name, type=exhange_type),
                           routing_key=routing_key
            )

    def get_consumers(self, Consumer, channel):

        return [
            Consumer(queues=self.task_queue, on_message=self.on_request,
            accept={'application/json'}, prefetch_count=1,)
        ]
    
    def process_task(self, body, message):

        message.ack()

class PayloadProcessor(ConsumerProducerMixin):

    def __init__(self, connection, exchange_name, queue_name, 
                 routing_key, exchange_reply, exhange_type='topic'):
        
        self.connection = connection
        self.exchange_reply = Exchange(exchange_reply, type='direct')
        self.queue = Queue(queue_name, 
                           Exchange(exchange_name, type=exhange_type),
                           routing_key=routing_key
            )

    def get_consumers(self, Consumer, channel):

        return [
            Consumer( queues=self.queue, on_message=self.on_request,
            accept={'application/json'}, prefetch_count=1,)
        ]

    def on_request(self, message):
        n = message.payload['n']
        print(' [.] fib({0})'.format(n))
        result = fib(n)

        self.producer.publish(
            {'result': result},
            exchange= self.exchange_reply, routing_key=message.properties['reply_to'],
            correlation_id=message.properties['correlation_id'],
            serializer='json',
            retry=True,
        )
        message.ack()


def payload_consumer(queue_name, routing_key, payload, 
                      exchange_name='backend-service'):
    
    task_queue = Queue(queue_name, Exchange(exchange_name, type='direct'), 
                       routing_key=routing_key)

    def callback(body, message):
        print('RECEIVED MESSAGE: {0!r}'.format(body))
        message.ack()

    with Connection(BROKER_URI) as conn:
        with conn.channel() as channel:
            consumer = Consumer(conn, [task_queue], accept=['json'])
            consumer.register_callback(callback)
            with consumer:
                conn.drain_events(timeout=1)
