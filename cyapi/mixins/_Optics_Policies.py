from pprint import pprint

class Mixin:

    def get_rule_sets_to_policy_mapping(self, **kwargs):
        return self.get_list_items("opticsPolicies","/configurations", **kwargs)

    def update_ruleset_in_policy(self, ruleset, policy):
        '''Success Code: 200'''
        baseURL = self.baseURL + "opticsPolicies/v2/configurations"

        data = {
                "configuration_type": "DETECTION",
                "configuration_id": ruleset['id'],
                "link": [policy['policy_id'],],
                "unlink": []
                }

        if self.debug_level > 1:
            pprint(data)

        return self._make_request("post",baseURL, data=data)

    def remove_policy_from_ruleset(self, ruleset, policy_id):
        baseURL = self.baseURL + "opticsPolicies/v2/configurations"

        data = {
                "configuration_type": "DETECTION",
                "configuration_id": ruleset['id'],
                "link": [],
                "unlink": [policy_id,]
                }

        return self._make_request("post",baseURL, data=data)

    def get_ruleset_for_policy(self, policy_id):
        baseURL = self.baseURL + "opticsPolicies/v2/configurations/{}".format(policy_id)

        return self._make_request("get",baseURL)
