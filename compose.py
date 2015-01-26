from botutils import images as Image
from db import DB
from common import redis_init
from tweet import Twy_REST

def get_untweeted_record():
    redis = redis_init()

    new_record = None
    while not new_record:
        record = DB().retrieve_record()

        if not redis.sismember('tweeted_oids', record.order_no):
            new_record = record
            redis.sadd('tweeted_oids', record.order_no)

    return new_record

def format_name(full_name):
    print full_name
    raw_name    = full_name.strip('.')
    names       = raw_name.split(', ')

    names.reverse()

    return " ".join(names)

def compose_message(record):
    print record.__dict__
    title   = record.title.strip()
    date   = record.date.strip()
    url     = record.image_url.strip()

    if record.photographer:
        photog  = format_name(record.photographer)
        message = "{0}, {1} | photo: {2} | LAPL collection: {3}".format(title, date, photog, url)
    else:
        message = "{0}, {1} | LAPL collection: {2}".format(title, date, url)

    return message


if __name__ == "__main__":
    record = get_untweeted_record()

    img = Image.get_image_from_url(record.image_url)
    img_path = Image.save_and_get_image_path(img)

    message = compose_message(record)

    Twy_REST().update_status_with_media(message, img_path)
