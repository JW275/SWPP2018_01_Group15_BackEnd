from config import allowed_hosts

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Access-Control-Allow-Origin'] = allowed_hosts
        response['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, PUT, OPTIONS'
        response['Access-Control-Max-Age'] = 1000
        response['Access-Control-Allow-Headers'] = 'origin, content-type, accept, Authorization, Set-Cookie'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
