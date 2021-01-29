import json
import re
import requests  # requests version 2.18.4 as of the time of authoring.


class Mixin:

    def get_mtc_health_check(self, **kwargs):
        """Gets MTC API Operational State
        No Authorization is required
        Sample Data Returned: {"Version: 0.81.480.0 | Environment: 'Production'"}
        """
        baseURL = self.baseURL + "health-check"

        response = requests.get(baseURL)


        return ApiResponse(response)

class ApiResponse:
    def __init__(self, response):
        self.status_code = response.status_code
        self.is_success = response.status_code < 300
        self.data = None
        self.errors = None

        if self.status_code == 429:
            print("API Rate Limited")

        if self.is_success:
            try:
                #The try/except and re.sub lines accept the
                # non-json values/messages when a successful response
                # is sent. This seems unique to the HealthCheck endpoint.
                # This should omit a 'None' data response.
                try:
                    self.data = response.json()
                except json.decoder.JSONDecodeError:
                    self.data = re.sub('{|"|}', "",response.text)
            except json.decoder.JSONDecodeError:
                self.data = None

        else:
            try:
                self.errors = response.json()
            except json.decoder.JSONDecodeError:
                self.errors = None

    def to_json(self):
        return {'is_success': self.is_success, 'data': self.data, 'errors': self.errors}
