import time
from datetime import datetime
import compose

def manual_tweet():
    tweet = assemble_tweet()
    Twy_REST().update_status_with_media(*tweet)


if __name__ == "__main__":

    # '''Run tweets five-ish times daily during work hours'''
    while True:

        current_hour = datetime.now().hour
        if current_hour >= 7 and current_hour <= 19:
            try:
                # assmble tweet
                tweet = assemble_tweet()

                if not env_is_dev:
                    Twy_REST().update_status_with_media(*tweet)

                # tweet again in three hours
                time.sleep(8640)

            except Exception as e:
                logging.exception(e)
                time.sleep(60)
        else:
            # tweet again in ten min
            time.sleep(600)
