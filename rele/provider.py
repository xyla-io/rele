from redis import Redis
from typing import List
from time import sleep

class Provider:
  r: Redis
  broadcast_channel: str

  def __init__(self, redis: Redis, broadcast_channel: str):
    self.r = redis
    self.broadcast_channel = broadcast_channel
  
  def feed(self, data: str):
    self.r.publish(self.broadcast_channel, data)

class BatchProvider(Provider):
  queue: List[str]
  batch_size: int
  rate: float
  delay: float

  def __init__(self, redis: Redis, broadcast_channel: str, batch_size: int, rate: float, delay: float=0):
    self.queue = []
    self.batch_size = batch_size
    self.rate = rate
    self.delay = delay
    super().__init__(
      redis=redis,
      broadcast_channel=broadcast_channel
    )

  def enqueue(self, chunks: List[str]):
    self.queue.extend(chunks)
    if self.delay > 0:
      sleep(self.delay)
      
    chunk_index = 0
    batch = ''
    def feed_batch():
      nonlocal chunk_index, batch
      if not chunk_index:
        return
      self.feed(batch)
      chunk_index = 0
      batch = ''
      if self.rate > 0:
        sleep(self.rate)

    for chunk in chunks:
      chunk_index = chunk_index + 1
      if chunk_index < self.batch_size:
        batch = batch + chunk
        continue
      feed_batch()
    feed_batch()
