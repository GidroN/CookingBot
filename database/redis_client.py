import logging
import redis
from redis.exceptions import ConnectionError


class RedisClient:
    """ Class to get connected client without repeat connection """

    def __init__(self):
        self.client: redis.Redis = ...
        self.host: str = ...
        self.port: str = ...
        self.db: str = ...

    def connect(self, *args, **kwargs):
        self.client = redis.Redis(*args, **kwargs)
        self.check_connection()

        self.host = kwargs['host']
        self.port = kwargs['port']
        self.db = kwargs.get('db') or 0

        logging.info('Redis connected.')

    def check_connection(self):
        try:
            self.client.ping()
        except ConnectionError:
            logging.error('Error while connecting to redis.')
            raise ConnectionError

    def disconnect(self):
        if self.client:
            self.client.close()
            logging.info('Redis disconnected.')
        else:
            logging.warning('Could\'t close redis connection. Redis isn\'t connected.')

    def get_url(self):
        return f'redis://{self.host}:{self.port}/{self.db}'

    def get_client(self):
        return self.client


rc = RedisClient()
