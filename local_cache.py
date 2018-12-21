# coding:utf-8
__author__ = 'qiuyujiang'

from time import time
from collections import deque


class LocalCache:
    def __init__(self, max_length, expire_seconds):
        self.cache = {}
        # 存key的队列，FIFO原则，越靠左的是越新的key，越靠右的是越早的key
        self.key_queue = deque(maxlen=max_length)
        self.max_length = max_length
        self.expire_seconds = expire_seconds

    def remove_expired_cache(self):
        if len(self.key_queue) == 0:
            return

        now = int(time())
        earliest_key = self.key_queue.pop()

        if earliest_key not in self.cache:
            return

        is_earliest_key_expired = self.cache[earliest_key]['expire_time'] < now
        while is_earliest_key_expired:
            self.cache.pop(earliest_key)
            if len(self.key_queue) == 0:
                break
            else:
                earliest_key = self.key_queue.pop()
                is_earliest_key_expired = self.cache[earliest_key]['expire_time'] < now
        if not is_earliest_key_expired:
            self.key_queue.append(earliest_key)

    def get(self, key):
        self.remove_expired_cache()
        if key in self.cache:
            return self.cache[key]['val']
        return None

    def set(self, key, value):
        self.remove_expired_cache()
        if len(self.key_queue) == self.max_length:
            earliest_key = self.key_queue.pop()
            self.cache.pop(earliest_key)
        now = int(time())
        self.key_queue.appendleft(key)
        self.cache[key] = {'val': value, 'expire_time': (now + self.expire_seconds)}
