from twython import Twython
import arrow

from textreader import APP_KEY, APP_SECRET, OAUTH_TOKEN_SECRET, OAUTH_TOKEN


def lambda_handler(event, context):
    api = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    text = arrow.now().to(tz="Europe/Helsinki").isoformat()

    api.update_status(status=text)

    # TODO implement
    return {"message": "OK", "text": text}
