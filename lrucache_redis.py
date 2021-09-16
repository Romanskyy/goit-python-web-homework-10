import redis 
db = redis.Redis(host = 'localhost', port = 6379, db = 0)

class LruCache:

    def __init__(self, func, max_size, db):
        self.max_size = max_size
        self.db = db
        self.func = func

    def __call__(self):
        pass