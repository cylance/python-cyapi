
class Mixin:

    def add_to_global_list(self, global_list, reason, sha256, category="None"):
        if global_list.lower() == "safe":
            list_type = "GlobalSafe"
        elif global_list.lower() == "quarantine":
            list_type = "GlobalQuarantine"
        else:
            raise ValueError("global_list must be 'safe' or 'quarantine'")

        categories = ["AdminTool", "CommercialSoftware", "Drivers", "internalApplication", "OperatingSystem", "SecuritySoftware", "None"]
        if category not in categories:
            raise ValueError("Category must be one of: {}".format(categories))

        data = {
            "sha256": sha256.lower(),
            "list_type": list_type,
            "category": category,
            "reason": reason
        }

        baseURL = self.baseURL + "globallists/v2"
        return self._make_request("post",baseURL, data=data)

    def delete_from_global_list(self, global_list, sha256):
        if global_list.lower() == "safe":
            list_type = "GlobalSafe"
        elif global_list.lower() == "quarantine":
            list_type = "GlobalQuarantine"
        else:
            raise ValueError("global_list must be 'safe' or 'quarantine'")

        data = {
            "sha256": sha256.lower(),
            "list_type": list_type,
        }

        baseURL = self.baseURL + "globallists/v2"
        return self._make_request("delete",baseURL, data=data)

    def get_global_list(self, global_list, **kwargs):

        if global_list.lower() == "quarantine":
            type_id = 0
        elif global_list.lower() == "safe":
            type_id = 1
        else:
            raise ValueError("global_list value must be 'safe' or 'quarantine'")

        params = {"listTypeId": type_id}
        return self.get_list_items('globallists',limit=20, params=params, **kwargs)
