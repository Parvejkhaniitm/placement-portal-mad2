import json
import redis


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=1,
    decode_responses=True
)


def get_cache(key):
    cached_data = redis_client.get(key)

    if not cached_data:
        return None

    return json.loads(cached_data)


def set_cache(key, value, timeout=60):
    redis_client.setex(
        key,
        timeout,
        json.dumps(value)
    )


def delete_cache(key):
    redis_client.delete(key)