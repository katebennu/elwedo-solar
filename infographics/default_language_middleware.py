from django.utils import translation

from django.utils.deprecation import MiddlewareMixin


DOMAIN_LANGUAGE_MAP = {
    "elwedo.com": "en",
    "elwedo.fi": "fi"
}


class DefaultLanguageMiddleware(MiddlewareMixin):

    def process_request(self, request):
        site = request.META['HTTP_HOST'].split(":")[0]
        if translation.LANGUAGE_SESSION_KEY not in request.session:
            request.session[translation.LANGUAGE_SESSION_KEY] = DOMAIN_LANGUAGE_MAP.get(site, "en")
