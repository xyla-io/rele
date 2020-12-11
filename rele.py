import redis

from environment import get_option
from pathlib import Path

redis_client = redis.Redis(**get_option('redis'))

from rele import BatchProvider, ProviderStreamInfo

data_path = Path(__file__).parent / 'output' / 'fabrica' / 'xy.csv'
data = data_path.read_text()
chunks = [c + '\n' for c in data.split('\n')[1:-1]]

stream_info = ProviderStreamInfo(
  key='RELE_BROADCAST_STREAM',
  metadata={
    'source': 'rele_script',
  }
)

provider = BatchProvider(
  redis=redis_client,
  broadcast_channel='RELE_BROADCAST_CHANNEL',
  batch_size=10,
  rate=1,
  delay=3,
  stream_info=stream_info
)
provider.enqueue(chunks=chunks)