import random
from twython import Twython
from config.common import twitter_cred, env_is_dev

class Twy_REST(object):
    '''If run on remote, completes action via Twython and prints output. /
        Otherwise, if run locally, only prints to terminal.'''

    def __init__(self):
        self.twitter = Twython(*twitter_cred)

    def update_status_with_media(self, text, img_path):
        # create temp file
        with open(img_path, 'r') as image_file:
            logging.info("Uploading Image: %s" % img_path)

            upload_response = self.twitter.upload_media(media=image_file)
            logging.info("Uploaded as media ID %s. Updating status." % upload_response)

            media_id = upload_response['media_id']

            time.sleep(10)

            if not env_is_dev:
                self.twitter.update_status(
                    status=message,
                    media_ids=[media_id])
