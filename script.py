import bot.compose as compose
from bot.tweet import Twy_REST

def manual_tweet():
    tweet = compose.assemble_tweet()
    Twy_REST().update_status_with_media(*tweet)

def test_tweet():
    tweet = compose.assemble_tweet()
    print(tweet)
