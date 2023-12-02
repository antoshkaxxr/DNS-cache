import pickle
import time


class CacheWorker:
    def __init__(self):
        self.cache = self.load_cache()

    def save_cache(self):
        with open('dns_cache.pickle', 'wb') as file:
            pickle.dump(self.cache, file)

    @staticmethod
    def load_cache():
        try:
            with open('dns_cache.pickle', 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def get_cached_response(self, request):
        cache_key = str(request.question[0].QNAME)
        if cache_key in self.cache:
            record = self.cache[cache_key]
            if time.time() < record.expiration_time:
                return record.response
            else:
                del self.cache[cache_key]
        return None
