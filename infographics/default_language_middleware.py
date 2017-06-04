from django.utils import translation
from django.conf import settings


DOMAIN_LANGUAGE_MAP = {
    "elwedo.com": "en",
    "elwedo.fi": "fi"
}


class DefaultLanguageMiddleware(object):

    def process_request(self, request):
        site = request.META['HTTP_HOST']
        if settings.LANGUAGE_COOKIE_NAME not in request.COOKIES:
            user_language = DOMAIN_LANGUAGE_MAP.get(site, "en")
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language
