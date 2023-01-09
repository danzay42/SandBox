
class CustomMiddleware:

    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request):
        print("Custom middleware, before")
        response = self._get_response(request)
        print("Custom middleware, after")
        return response

    # def process_exception(self, request, exception):
    #     print(f"Exception is {exception}")
