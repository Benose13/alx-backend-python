import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file.
    Logs timestamp, user, and the request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler("requests.log")  # file to log requests
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        # Identify user or anonymous
        user = request.user if request.user.is_authenticated else "AnonymousUser"
        
        # Create log entry
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_entry)

        # Continue the request/response cycle
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app
    outside of business hours (6AM - 9PM).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow access only between 6AM (6) and 9PM (21)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "❌ Access to the messaging app is restricted between 9PM and 6AM."
            )

        response = self.get_response(request)
        return response