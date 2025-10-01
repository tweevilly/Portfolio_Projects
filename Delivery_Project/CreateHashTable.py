#create hash map

class CreateHashMap:
    def __init__(self, initial_capacity=20):
        # Initialize buckets (lists of key-value pairs)
        self.buckets = [[] for _ in range(initial_capacity)]

    def _get_bucket(self, key):
        #get the bucket index for a given key
        return self.buckets[hash(key) % len(self.buckets)]

    def insert(self, key, item):
        #Insert or update a key-value pair
        bucket = self._get_bucket(key)

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, item)  # update existing
                return True

        bucket.append((key, item))  # insert new
        return True

    def lookup(self, key):
        #Retrieve value for a key, or None if not found
        bucket = self._get_bucket(key)
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key):
        #Remove key-value pair by key. Return True if removed
        bucket = self._get_bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False