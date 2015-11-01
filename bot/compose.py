import requests
import json
from botutils import images as Image
from config.common import redis_init, env_is_dev
from db import DB
from tweet import Twy_REST

def get_untweeted_record():
    redis = redis_init()

    new_record = None
    while not new_record:
        record = DB().retrieve_record()

        if not redis.sismember('tweeted_oids', record.order_no):
            new_record = record

    return new_record

def update_tweeted_oids(record):
    redis = redis_init()
    redis.sadd('tweeted_oids', record.order_no)

def format_name(full_name):
    print full_name
    raw_name    = full_name.strip('.')
    names       = raw_name.split(', ')

    names.reverse()

    return " ".join(names)

def format_info(info):
    info_array = info.split("\n")

    if len(info_array) > 2:
        return info_array[0].strip()
    else:
        return None


def compose_message(record):
    print record.__dict__
    title               = record.title.strip()
    collection_info     = format_info(record.filing_info)
    date                = record.date.strip()
    order_no            = record.order_no.strip()

    long_url            ="http://photos.lapl.org/carlweb/jsp/DoSearch?databaseID=968&count=10&terms={0}&index=w".format(order_no)
    url                 = shorten_url(long_url)

    message = "{0}, {1} ".format(title, date)

    if record.photographer:
        photog  = format_name(record.photographer)
        message += "photo {0} ".format(photog)
    if collection_info:
        message += "| {0} ".format(collection_info)
    else:
        message += "| "

    message += "{0}".format(url)

    return message

def shorten_url(url):
    '''Accepts a to-be shortened URL, then returns a shortened URL using
    Google's URL Shortener API.'''

    post_url = 'https://www.googleapis.com/urlshortener/v1/url'
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}

    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    r_hash = r.json()

    return r_hash['id']

def assemble_tweet():
    record = get_untweeted_record()
    message = compose_message(record)

    # continue to get records until of tweetable length
    while len(message) > 140:
        print "Generated tweet too long. Creating another."
        record = get_untweeted_record()
        message = compose_message(record)

    img = Image.get_image_from_url(record.image_url)
    img_path = Image.save_and_get_image_path(img)

    update_tweeted_oids(record)

    params = [message, img_path]

    return params
