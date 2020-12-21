
class Mixin:

    def get_detection_rule(self, rule_id, natlang=False):
        # /rules/v2/{rule_id}
        if natlang == True:
            baseURL = self.baseURL + "rules/v2/{}/natlang".format(rule_id)
            return self._make_request("get",baseURL)

        return self.get_item("rules", rule_id)

    def get_bulk_detection_rule(self, rule_ids, disable_progress=True):
        """Get rule detail for many IDs
        :param rule_ids: list of rule_ids
        """
        baseURL = self.baseURL + "rules/v2/{}"
        urls = []
        if isinstance(rule_ids, list):
            for rule in rule_ids:
                urls.append(baseURL.format(rule))
            return self._bulk_get(urls, paginated=False, disable_progress=disable_progress)

    def get_detection_rules(self, csv=False, **kwargs):
        # /rules/v2?page=m&page_size=n
        if csv:
            baseURL = self.baseURL + "rules/v2/csv"
            return self._make_request("get",baseURL)

        return self.get_list_items("rules", **kwargs)

    def get_detection_rule_counts(self, rule_id):
        # /rules/v2/{rule_id}/counts
        baseURL = self.baseURL + "rules/v2/{}/counts".format(rule_id)
        return self._make_request("get",baseURL)

    def validate_detection_rule(self, rule_data):
        # /rules/v2/validate
        baseURL = self.baseURL + "rules/v2/validate"
        return self._make_request("post",baseURL, data=rule_data)

    def create_detection_rule(self, rule_data):
        # /rules/v2
        baseURL = self.baseURL + "rules/v2"
        return self._make_request("post",baseURL, data=rule_data)

    def update_detection_rule(self, rule_id, rule_data):
        # /rules/v2/{rule_id}
        baseURL = self.baseURL + "rules/v2/{}".format(rule_id)
        return self._make_request("put",baseURL, data=rule_data)

    def deactivate_detection_rule(self, rule_id):
        # /rules/v2/{rule_id}/deactivate
        baseURL = self.baseURL + "rules/v2/{}/deactivate".format(rule_id)
        return self._make_request("post",baseURL)
