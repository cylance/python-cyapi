
class Mixin:

    def get_detection_exceptions(self, csv=False, **kwargs):
        # /exceptions/v2
        #/exceptions/v2/csv
        if csv:
            baseURL = self.baseURL + "exceptions/v2/csv"
            return self._make_request("get",baseURL)

        return self.get_list_items("exceptions",**kwargs)

    def get_detection_exception(self, exc_id):
        # /exceptions/v2/{exception_id}
        baseURL = self.baseURL + "exceptions/v2/{}".format(exc_id)
        return self._make_request("get",baseURL)

    def create_detection_exception(self, exception_data):
        # /exceptions/v2
        baseURL = self.baseURL + "exceptions/v2"
        return self._make_request("post",baseURL, data=exception_data)

    def update_detection_exception(self, exception_id, exception_data):
        # /exceptions/v2/{exception_id}
        baseURL = self.baseURL + "exceptions/v2/{}".format(exception_id)
        return self._make_request("put",baseURL, data=exception_data)

    def deactivate_detection_exception(self, exception_id):
        # /exceptions/v2/{exception_id}/deactivate
        baseURL = self.baseURL + "exceptions/v2/{}/deactivate".format(exception_id)
        return self._make_request("post",baseURL)
