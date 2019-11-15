import json
import time
from pprint import pprint

class Mixin:
    # Method to clone an IQ for fresh results. Takes existing IQ ID and returns Cloned IQ ID.
    def clone_iq(self, query_id, new_name, new_description=""):
        response = self.get_instaquery(query_id)
        old_iq = response.json()
        if self.debug_level > 1:
            for name in old_iq:
                print( name, ": ", old_iq[name] )

        new_iq = self.create_instaquery(new_name, new_description, old_iq['artifact'], old_iq['match_value_type'], old_iq['match_values'], old_iq['case_sensitive'], old_iq['zones'] )
        return new_iq

    # Generic method to generate an InstaQuery request
    def create_instaquery(self, query_name, query_description, artifact_type, facet_type, match_values, case_sensitive, zones):
        baseURL = self.baseURL + "instaqueries/v2"
        requestBody = {
            "name": query_name,
            "description": query_description,
            "artifact": artifact_type,
            "match_value_type": facet_type,
            "match_values": match_values,
            "case_sensitive": case_sensitive,
            "match_type": "Fuzzy",
            "zones": zones
        }

        if self.debug_level > 2:
            pprint( requestBody )

        return self._make_request("post",baseURL, data=requestBody)

    def get_instaqueries(self, q=None, archived=None, origin_from=None, **kwargs):
        params = {
            "q": q,
            "archived": archived,
            "originated-from": origin_from
        }

        return self.get_list_items("instaqueries", params=params, **kwargs)

    def get_instaquery_results(self, iq_id):
        baseURL = self.baseURL + "instaqueries/v2/{}/results".format(iq_id)
        return self._make_request("get",baseURL)

    # Method to retrieve an InstaQuery
    def get_instaquery(self, query_id):
        baseURL = self.baseURL + "instaqueries/v2/{}".format(query_id)

        return self._make_request("get",baseURL)

    def archive_instaquery(self, query_id):
        """endpoint: /instaqueries/v2{queryID}/archive
        """
        baseURL = self.baseURL + "instaqueries/v2/{}/archive".format(query_id)
        return self._make_request("post",baseURL)
