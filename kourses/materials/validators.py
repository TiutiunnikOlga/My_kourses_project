from urllib.parse import urlparse

from rest_framework.exceptions import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field
        self.allowed_domains = {"youtube.com"}

    def __call__(self, value):
        link = value.get(self.field)
        if link is None:
            raise ValidationError(f'Поле "{self.field}" не может быть пустым.')

        if not isinstance(link, str):
            raise ValidationError(f'Поле "{self.field}" должно быть строкой.')

        link = link.strip()
        parsed = urlparse(link)
        if not parsed.scheme or not parsed.netloc:
            raise ValidationError("Link not from youtube.com")
