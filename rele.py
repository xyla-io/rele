import redis

from environment import get_option

redis_client = redis.Redis(**get_option('redis'))

from rele import Provider

provider = Provider(
  redis=redis_client,
  broadcast_channel='RELE_BROADCAST_CHANNEL'
)
provider.feed(data='1,2\n3,4\n5,6\n7,8')