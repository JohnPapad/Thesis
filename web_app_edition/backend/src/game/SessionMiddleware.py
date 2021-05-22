from django.contrib.sessions.middleware import SessionMiddleware
# used to bypass the Session middleware when the web_app is used.
# Django needs that kinf od middleware so we create a class that extends the default middleware.

class DisableSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        request.session = {}
        if request.path_info.startswith('/web_app/'):
            return
        super(DisableSessionMiddleware, self).process_request(request)

    def process_response(self, request, response):
        if request.path_info.startswith('/web_app/'):
            return response
        return super(DisableSessionMiddleware, self).process_response(request, response)