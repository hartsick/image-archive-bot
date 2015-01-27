import os
import redis

twitter_cred = [
    os.environ.get('MASTER_BOT_CONSUMER_KEY'),
    os.environ.get('MASTER_BOT_CONSUMER_SECRET'),
    os.environ.get('LAPL_ACCESS_TOKEN'),
    os.environ.get('LAPL_ACCESS_TOKEN_SECRET')
]

env_is_dev = True if os.environ.has_key('USER') else False

# Set DB url
if env_is_dev:
    db_cred = os.getenv('DATABASE_URL', 'postgresql://localhost/lapl_bot')
else:
    db_cred = os.environ.get('DATABASE_URL')

def redis_init():

    # Redis Init
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    r = redis.from_url(redis_url)

    return r
