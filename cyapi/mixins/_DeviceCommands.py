
class Mixin:

    def get_retrieved_file_results(self, **kwargs):
        # /devicecommands/v2/retrieved_files?page=m&page_size=n
        return self.get_list_items("devicecommands", detail="/retrieved_files", **kwargs)

    # Get Detection, might need better way to get additional detection pages
    def lockdown_device(self, device_id, exp):
        # exp = expires: Duration of the lockdown. Format: 'd:hh:mm'
        device_id = self._convert_id(device_id)
        params = {"value":"true", "expires": exp}
        baseURL = self.baseURL + "devicecommands/v2/{}/lockdown".format(device_id)
        baseURL = self._add_url_params(baseURL, params)

        return self._make_request("get",baseURL)

    # Get Detection, might need better way to get additional detection pages
    def get_device_lockdown_history(self, device_id):

        device_id = self._convert_id(device_id)
        baseURL = self.baseURL + "devicecommands/v2/{}/lockdown".format(device_id)

        return self._make_request("get",baseURL)

    def request_file_retrieval_from_device(self, device_id, file_path):
        # /devicecommands/v2/{{device_id}}/getfile
        device_id = self._convert_id(device_id)
        baseURL = self.baseURL + "devicecommands/v2/{}/getfile".format(device_id)
        data =  { "file_path": file_path }
        return self._make_request("post",baseURL, data=data)

    def check_file_retrieval_status_from_device(self,device_id, file_path):
        # /devicecommands/v2/{{device_id}}/getfile:get
        device_id = self._convert_id(device_id)
        baseURL = self.baseURL + "devicecommands/v2/{}/getfile:get".format(device_id)
        data = { "file_path": file_path }
        return self._make_request("post",baseURL, data=data)
