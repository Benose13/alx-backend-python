import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, JsonResponse

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


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of chat messages
    (POST requests) per minute from a single IP address.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = {}  # {ip: [timestamps]}
        self.message_limit = 5  # Max messages allowed per minute
        self.time_window = timedelta(minutes=1)

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Only apply to POST requests (e.g., sending chat messages)
        if request.method == "POST" and "/messages" in request.path:
            now = datetime.now()
            timestamps = self.message_logs.get(ip, [])

            # Remove timestamps older than 1 minute
            timestamps = [t for t in timestamps if now - t < self.time_window]

            if len(timestamps) >= self.message_limit:
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded. You can only send 5 messages per minute."
                    },
                    status=429,
                )

            # Record the new message timestamp
            timestamps.append(now)
            self.message_logs[ip] = timestamps

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Retrieve client's IP address from request headers."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolePermissionMiddleware:
    """
    Middleware to restrict access based on user roles.
    Only users with 'admin' or 'moderator' roles are allowed to access restricted endpoints.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define which paths require admin/moderator access
        restricted_paths = [
            "/api/admin/",
            "/admin/",
            "/api/conversations/",
        ]

        # Only check for restricted paths
        if any(request.path.startswith(path) for path in restricted_paths):
            user = getattr(request, "user", None)

            if not user or not user.is_authenticated:
                return JsonResponse(
                    {"error": "Authentication required."}, status=401
                )

            # Check role attribute on your User model
            role = getattr(user, "role", None)

            if role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"error": "Forbidden: insufficient permissions."}, status=403
                )

        response = self.get_response(request)
        return response