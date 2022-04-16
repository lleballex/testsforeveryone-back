from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from rest_framework.serializers import ImageField

from base64 import b64decode


class ImageField(ImageField):
    def to_internal_value(self, data):
        if not data: return None
        
        frmt, img_str = data.split(';base64,')
        extension = frmt.split('/')[-1]
        image = ContentFile(b64decode(img_str),
                            name=f'{get_random_string(length=6)}.{extension}')
        return super().to_internal_value(image)



from django.utils import timezone
from rest_framework.serializers import ReadOnlyField

from datetime import timedelta


MONTHS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
          'августа', 'сентября', 'октября', 'ноября', 'декабря']


def get_past_time(count, hours=False, minutes=False):
    assert hours or minutes

    if count == 1:
        return f'1 {"час" if hours else "минуту"} назад'
    if count <= 4:
        return f'{count} {"часа" if hours else "минуты"} назад'
    return f'{count} {"часов" if hours else "минут"} назад'


def get_date(date):
    now = timezone.localtime()
    date = timezone.localtime(date)

    if now.month == date.month and now.year == date.year and \
            (now.day == date.day or (now - timedelta(days=1)).day == date.day):
        seconds = int((now - date).total_seconds())
        minutes = seconds // 60
        hours = minutes // 60

        if minutes < 1:
            return 'только что'

        if hours < 1:
            return f'{get_past_time(minutes, minutes=True)}'

        if hours <= 10:
            return f'{get_past_time(hours, hours=True)}'

        if now.day == date.day:
            return 'сегодня'

        return 'вчера'

    return f'{date.day} {MONTHS[date.month]}'



class DateTimeField(ReadOnlyField):
    def to_representation(obj, value):
        return get_date(value)