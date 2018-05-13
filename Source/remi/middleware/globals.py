from threading import current_thread


class GlobalRequest(object):

    _requests = {}

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        thread = current_thread()

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        GlobalRequest._requests[thread] = request

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        try:
            if request is not None:
                del GlobalRequest._requests[thread]
        except KeyError:
            pass

        return response

    @staticmethod
    def get_request():
        try:
            return GlobalRequest._requests[current_thread()]
        except KeyError:
            return None

