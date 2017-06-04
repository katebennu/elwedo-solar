from django.utils import translation

from django.utils.deprecation import MiddlewareMixin


DOMAIN_LANGUAGE_MAP = {
    "elwedo.com": "en",
    "elwedo.fi": "fi"
}


class DefaultLanguageMiddleware(MiddlewareMixin):

    def process_request(self, request):
        site = request.META['HTTP_HOST'].split(":")[0]
        if "sessionid" not in request.COOKIES:
            user_language = DOMAIN_LANGUAGE_MAP.get(site, "en")
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language
