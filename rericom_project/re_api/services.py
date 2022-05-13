import os
import kafka
from json import dumps, loads


class KafkaSender():
    __slots__ = 'producer', 'output_topic', 'bootstrap_servers',

    def __init__(self,
                 bootstrap_servers,
                 output_topic):
        self.output_topic = output_topic
        self.bootstrap_servers = bootstrap_servers

    def start(self):
        self.producer = kafka.KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                            value_serializer=lambda v: dumps(v).encode('utf-8'))

    def send_message(self, output: dict):
        self.producer.send(self.output_topic, output)
        if os.getenv('ENV', 'DEV') == 'DEV':
            self.producer.flush()
