from collection.models import RequestServe


class RequestLog:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Create instance of our model and assign values
        request_log = RequestServe(
            endpoint=request.get_full_path()
        )

        if not request.user.is_anonymous:
            request_log.user = request.user
        # Save log in db
        request_log.save()
        return response
