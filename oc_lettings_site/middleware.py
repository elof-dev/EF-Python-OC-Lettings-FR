import logging
from django.http import Http404
from sentry_sdk import capture_message

logger = logging.getLogger(__name__)

class Capture404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Http404:
            logger.warning("404 at %s", request.path)
            capture_message(f"404 at {request.path}", level="warning")
            raise
