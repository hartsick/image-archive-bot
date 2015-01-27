import time
from datetime import datetime
import bot.compose as compose
from bot.tweet import Twy_REST

if __name__ == "__main__":

    # '''Run tweets five-ish times daily during work hours'''
    while True:

        current_hour = datetime.now().hour
        if current_hour >= 7 and current_hour <= 19:
            try:
                # assmble tweet
                tweet = compose.assemble_tweet()

                Twy_REST().update_status_with_media(*tweet)

                # tweet again in three hours
                time.sleep(8640)

            except Exception as e:
                print(e)
                time.sleep(60)
        else:
            # tweet again in ten min
            time.sleep(600)
