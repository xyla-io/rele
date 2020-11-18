from redis import Redis

class Provider:
  r: Redis
  broadcast_channel: str

  def __init__(self, redis: Redis, broadcast_channel: str):
    self.r = redis
    self.broadcast_channel = broadcast_channel
  
  def feed(self, data: str):
    self.r.publish(self.broadcast_channel, data)