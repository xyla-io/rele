from redis import Redis
from typing import List, Optional, Dict
from time import sleep

class ProviderStreamInfo:
  key: str
  metadata: Dict[str, str]

  def __init__(self, key: str, metadata: Dict[str, str]={}):
    self.key = key
    self.metadata = metadata

  def add(self, redis: Redis, data: str, metadata: Dict[str, str]={}):
    redis.xadd(self.key, {**self.metadata, **metadata, 'data': data})

class Provider:
  r: Redis
  broadcast_channel: str
  stream_info: Optional[ProviderStreamInfo]

  def __init__(self, redis: Redis, broadcast_channel: str, stream_info: Optional[ProviderStreamInfo]=None):
    self.r = redis
    self.broadcast_channel = broadcast_channel
    self.stream_info = stream_info
  
  def feed(self, data: str, metadata: Dict[str, str]={}):
    self.r.publish(self.broadcast_channel, data)
    if self.stream_info:
      self.stream_info.add(
        redis=self.r,
        data=data,
        metadata=metadata
      )

class BatchProvider(Provider):
  queue: List[str]
  batch_size: int
  rate: float
  delay: float
  batch_count: int

  def __init__(self, redis: Redis, broadcast_channel: str, batch_size: int, rate: float, delay: float=0, stream_info: Optional[ProviderStreamInfo]=None):
    self.queue = []
    self.batch_size = batch_size
    self.rate = rate
    self.delay = delay
    self.batch_count = 0
    super().__init__(
      redis=redis,
      broadcast_channel=broadcast_channel,
      stream_info=stream_info
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
      self.batch_count = self.batch_count + 1
      self.feed(
        data=batch,
        metadata={'batch': str(self.batch_count)}
      )
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
