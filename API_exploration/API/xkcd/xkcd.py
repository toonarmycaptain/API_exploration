"""xkcd API"""
from datetime import date, datetime
from typing import Union
from functools import lru_cache

import requests


@lru_cache(maxsize=128)
def get_comic_data(comic_number: Union[int, str]|None = None,
                   day: date = date.today(),
                   cache_hour: tuple[date, int] = (date.today(), datetime.now().hour)) -> dict:
    """
    Calls xkcd API, returns necessary data as a dict.

    Also seeks latest_comic number for UI reference.

    cache_hour default arg a tuple of the current date/hour, to invalidate the
    cache each hour, preventing a previous latest comic from continuing to be
    cached as latest.

    NB Latest comic API call https://xkcd.com//info.0.json' works.

    NB 404 is not a xkcd comic number, return latest comic data.

    :param comic_number: int
    :param day: datetime.date object
    :param cache_hour: tuple (datetime.date, int)
    :return: dict
    """
    if comic_number is None:
        comic_number = ''
    # Eventually handle this differently, possibly with a special page?
    elif int(comic_number) == 404:
        comic_number = ''

    with requests.Session() as session:
        comic_json = session.get(f'https://xkcd.com/{comic_number}/info.0.json').json()
        comic_data = {'comic_number': comic_json['num'],
                      'comic_url': f'https://xkcd.com/{comic_number}',
                      'comic_image_url': comic_json['img'],
                      'comic_title': comic_json['title'],
                      'comic_alt_text': comic_json['alt'],
                      'latest_comic_number': comic_json['num']
                      }
        if comic_number:  # ie if comic is not default/latest comic
            latest_comic_json = session.get(f'https://xkcd.com/info.0.json').json()
            comic_data['latest_comic_number'] = latest_comic_json['num']

    return comic_data
