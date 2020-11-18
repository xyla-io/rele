import redis

from environment import get_option

redis_client = redis.Redis(**get_option('redis'))

print(get_option('redis'))
print(redis_client.keys())

# from rele import Provider
# provider = Provider(redis_client)