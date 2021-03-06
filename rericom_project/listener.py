from json import dumps, loads
from decouple import config
import logging
import requests
import kafka
import jwt
import re

# log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class KafkaListener:
    __slots__ = 'bootstrap_servers', 'input_topic', 'consumer_group', 'consumer'

    def __init__(self,
                 bootstrap_servers,
                 input_topic: str,
                 consumer_group: str):
        self.bootstrap_servers = bootstrap_servers
        self.input_topic = input_topic
        self.consumer_group = consumer_group

    def start(self):
        self.consumer = kafka.KafkaConsumer(
            self.input_topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.consumer_group,
            enable_auto_commit=False,
            auto_commit_interval_ms=0,
            auto_offset_reset="earliest",
        )
        try:
            for message in self.consumer:
                self.consumer.commit()
                logging.info('message received')
                parsed_message = loads(message.value.decode('utf-8'))
                send_validated_resp(data=parsed_message, pattern= '.*абракадабра.*')

        finally:
            self.consumer.stop()


def send_validated_resp(data, pattern):
    if re.match(pattern, data.get('text').lower()):
        success = False
    else:
        success = True

    data_to_send = {
        'id': data.get('message_id'),
        'success': success
    }

    role = {
        "post_message_confirm": True,
    }
    token = jwt.encode(role, config('SECRET_JWT'), algorithm="HS256")
    headers = {
        'Authorization': token
    }
    requests.post(url='http://0.0.0.0:8000/api/v1/message_confirmation/', headers=headers, data=data_to_send)
    logging.info('Message posted')


if __name__ == "__main__":
    consumer = KafkaListener(bootstrap_servers=config('BOOTSTRAP_SERVERS_LISTENER'),
                             input_topic=config('KAFKA_TOPIC'), consumer_group='django')
    logging.info('Listening started')
    consumer.start()
