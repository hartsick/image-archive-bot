import os
import redis

twitter_cred = [
    os.environ.get('MASTER_BOT_CONSUMER_KEY'),
    os.environ.get('MASTER_BOT_CONSUMER_SECRET'),
    os.environ.get('LAPL_ACCESS_TOKEN'),
    os.environ.get('LAPL_ACCESS_TOKEN_SECRET')
]

env_is_dev = True if os.environ.has_key('USER') else False

db_cred = os.environ.get('LAPL_DB_CRED')

def redis_init():

    # Redis Init
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    r = redis.from_url(redis_url)

    return r
