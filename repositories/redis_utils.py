import numpy as np
from redis import Redis
import json


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()


class RedisUtils:
    client = Redis

    def __init__(self, host):
        self.client = Redis(host=host)

    def save_to_redis(self, entity_name: str, identifier: str, data: dict):
        json_data = json.dumps(data, default=np_encoder, ensure_ascii=False)
        key = entity_name + ':' + identifier
        self.client.set(key, json_data)

    def get_from_redis(self, entity_name: str, identifier: str):
        key = str(entity_name) + ':' + str(identifier)
        value = self.client.get(key).decode('UTF-8')
        return json.loads(value)