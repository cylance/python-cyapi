import json
import os
import pkg_resources

class Mixin:

    def get_policy_templates(self, **kwargs):
        """Get a list of all MTC Device Policy Templates
        Returns: listData: [PolicyTemplates], totalCount
        """
        baseURL = self.baseURL + "policy-templates/list"
        return self._make_request("get",baseURL)

    def get_policy_template(self, policy_template_id):
        """Get MTC Policy Template Detail
        parms: Takes policy_template_id
        """
        return self.get_item("policy-templates", policy_template_id)

    def update_policy_template(self, policy):
        """ Update MTC Device Policy Template by policy_template_id
        """
        baseURL = self.baseURL + "policy-templates/{}".format(policy['policy_id'])

        policy['checksum'] = ""
        policy['policy_utctimestamp'] = ""

        data = {}
        data['modelDetails'] = policy
        data['name'] = policy['name']
        data['partnerId'] = self.app_id
        data['policyTemplateId'] = policy['policy_id']

        return self._make_request("put",baseURL, data=data)

    def delete_policy_template(self, policy_template_id):
        """Delete MTC Device Policy Template by policy_template_id"""
        baseURL = self.baseURL + "policy-templates/{}".format(policy_template_id)

        return self._make_request("delete",baseURL)

    def create_device_policy_template(self, policy_name, policy_data=None):
        """Create a MTC Device Policy Template
        """
        baseURL = self.baseURL + "policy-templates"

        if policy_data is None:

            f = pkg_resources.resource_stream('cyapi', "reqs/create_policy.json")
            data = json.loads(f.read().decode('utf-8'))
            f.close()

        else:
            data = {'modelDetails': policy_data}
            data['policy_id'] = ""
            data['modelDetails']['checksum'] = ""
            data['modelDetails']['policy_utctimestamp'] = ""


        data['modelDetails'] = data
        data['name'] = policy_name
        data['partnerId'] = self.app_id
        response = self._make_request("post",baseURL)

        return response

