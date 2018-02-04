import os
import random
import requests
import logging

util_logger = logging.getLogger('brandon.util')
util_logger.setLevel(logging.INFO)


def random_image():
    return 'brandon/' + random.choice(os.listdir('brandon/')),


def thanked(message):
    """
    Try to determine if brandon-bot was thanked in the previous message.
    Obviously at this point it is a very cursory check.
    :param message: Message to parse
    :return: True if thanked
    """
    if 'no thanks' in message or 'for nothing' in message:
        util_logger.info(str(message) + " : false")
        return False
    elif 'thank' in message:
        util_logger.info(str(message) + " : true")
        return True
    return False


def url_is_valid(url):
    """
    Uses the Requests library to attempt to access a url, and
    determines whether the url is valid by its response
    :param url: Address to check
    :return: True if url returns 200
    """
    try:
        o = requests.head(url, allow_redirects=True)
        if o.status_code == requests.codes.ok:
            util_logger.info(str(url) + " responded with " + str(o.status_code))
            return True
        else:
            return False
    except Exception:
        util_logger.warning("url " + str(url) + " did not respond with a 200")
    return False
