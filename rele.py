import redis

from environment import get_option
from pathlib import Path

redis_client = redis.Redis(**get_option('redis'))

from rele import BatchProvider

data_path = Path(__file__).parent / 'output' / 'fabrica' / 'xy.csv'
data = data_path.read_text()
chunks = [c + '\n' for c in data.split('\n')[1:-1]]

provider = BatchProvider(
  redis=redis_client,
  broadcast_channel='RELE_BROADCAST_CHANNEL',
  batch_size=10,
  rate=1,
  delay=3
)
provider.enqueue(chunks=chunks)