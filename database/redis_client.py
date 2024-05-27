import logging
import redis


class RedisClient:
    """ Class to get connected client without repeat connection """

    def __init__(self):
        self.client: redis.Redis = ...

    def connect(self, *args, **kwargs):
        self.client = redis.Redis(*args, **kwargs)
        logging.info('Redis connected.')

    def disconnect(self):
        if self.client:
            self.client.close()
            logging.info('Redis disconnected.')

    def get_client(self):
        return self.client


rc = RedisClient()
