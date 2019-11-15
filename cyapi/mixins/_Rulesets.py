
class Mixin:
    def create_detection_rule_set(self, ruleset_data):

        return self.create_item('rulesets', ruleset_data)

    def delete_rule_sets(self, ruleset_ids):
        # /rulesets/v2
        baseURL = self.baseURL + "rulesets/v2"
        data = { "ids": ruleset_ids }

        return self._make_request("delete",baseURL, data=data)

    def delete_rule_set(self, ruleset_id):
        '''Delete ruleset by ID'''
        baseURL = self.baseURL + "rulesets/v2/{}".format(ruleset_id)

        return self._make_request("delete",baseURL)

    def get_ruleset(self, ruleset_id):
        '''Return detailed Ruleset information'''
        ruleset = self.get_item("rulesets", ruleset_id)
        return ruleset

    def get_bulk_ruleset(self, ruleset_ids, disable_progress=True):
        """Get ruleset detail for many IDs
        :param ruleset_ids: list of ruleset_ids
        """
        baseURL = self.baseURL + "rulesets/v2/{}"
        urls = []
        if isinstance(ruleset_ids, list):
            for ruleset in ruleset_ids:
                urls.append(baseURL.format(ruleset))
            return self._bulk_get(urls, paginated=False, disable_progress=disable_progress)

    def get_rulesets(self, csv=False, **kwargs):
        if csv:
            rulesets = self.get_list_items("rulesets", detail="/csv", **kwargs)
        else:
            rulesets = self.get_list_items("rulesets", **kwargs)
        return rulesets

    def update_detection_rule_set(self, ruleset_id, ruleset):
        # TODO: Add niceties for validating a ruleset and stuff that you can update
        # /rulesets/v2/{ruleset_id}
        baseURL = self.baseURL + "rulesets/v2/{}".format(ruleset_id)
        return self._make_request("put",baseURL, data=ruleset)

    def retrieve_default_detection_rule_set(self):
        # /rulesets/v2/default
        baseURL = self.baseURL + "rulesets/v2/default"
        return self._make_request("get",baseURL)
