
class Mixin:

    def get_threats(self, start_time=None, end_time=None, **kwargs):
        '''Get a list of Threats'''
        if end_time and not start_time:
            raise ValueError("start_time must be set if using end_time parameter")
        params = {"start_time": start_time, "end_time": end_time}

        return self.get_list_items('threats', params=params, **kwargs)

    def get_threat_devices(self, sha256, **kwargs):
        # /threats/v2/{threat_sha256}/devices?page=m&page_size=n
        return self.get_list_items("threats", "/" + sha256 + "/devices", **kwargs)

    def get_threat(self, threat_id):
        '''Get threat Detail'''
        return self.get_item("threats", threat_id)

    def get_threat_download_url(self, sha256):
        baseURL = self.baseURL + "threats/v2/download/{}".format(sha256)

        return self._make_request("get",baseURL)
