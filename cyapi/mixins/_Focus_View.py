
class Mixin:

    def get_focus_view_summary(self, focus_id):
        # /foci/v2/{focus_id}
        baseURL = self.baseURL + "foci/v2/{}".format(focus_id)
        return self._make_request("get",baseURL)

    def get_focus_view_results(self, focus_id):
        # /foci/v2/{{focus_id}}/results
        baseURL = self.baseURL + "foci/v2/{}/results".format(focus_id)
        return self._make_request("get",baseURL)

    def get_focus_views(self, q=None, **kwargs):
        """q - case-insensitive search term"""
        # https://protectapi.cylance.com/foci/v2?page=1&page_size=100
        params = {}
        if q:
            params['q']= q
        return self.get_list_items("foci", params=params, **kwargs)

    def search_for_focus_view_results(self, uid, device_id):
        # /foci/v2/search
        baseURL = self.baseURL + "foci/v2/search"
        uid = self._convert_id(uid)
        device_id = self._convert_id(device_id)
        data = [
                {
                    "uid": uid,
                    "device_id": device_id
                }
               ]
        return self._make_request("post",baseURL, data=data)

    def request_focus_view(self, device_id, artifact_type, artifact_subtype,
                           value, threat_type, description):
        # /foci/v2
        self._is_valid_artifact_type(artifact_type)

        baseURL = self.baseURL + "foci/v2"
        device_id = self._convert_id(device_id)

        data = {
                "device_id": device_id,
                "artifact_type": artifact_type,
                "artifact_subtype": "Uid",
                "value": value,
                "threat_type": threat_type,
                "description": description
        }

        return self._make_request("post",baseURL, data=data)
