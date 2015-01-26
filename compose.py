from botutils import images as Image
from db import DB
from common import redis_init, env_is_dev
from tweet import Twy_REST

def get_untweeted_record():
    redis = redis_init()

    new_record = None
    while not new_record:
        record = DB().retrieve_record()

        if not redis.sismember('tweeted_oids', record.order_no):
            new_record = record
            if not env_is_dev:
                redis.sadd('tweeted_oids', record.order_no)

    return new_record

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
    url                 = record.image_url.strip()
    order_no            = record.order_no.strip()

    message = "{0}, {1} ".format(title, date)

    if record.photographer:
        photog  = format_name(record.photographer)
        message += "photo {0} ".format(photog)
    if collection_info:
        message += "| {0}, ".format(collection_info)
    else:
        message += "| "

    message += "LAPL #{0} {1}".format(order_no, url)

    print "Composed: {0}".format(message)
    return message


if __name__ == "__main__":
    record = get_untweeted_record()

    img = Image.get_image_from_url(record.image_url)
    img_path = Image.save_and_get_image_path(img)

    message = compose_message(record)

    if not env_is_dev:
        Twy_REST().update_status_with_media(message, img_path)
