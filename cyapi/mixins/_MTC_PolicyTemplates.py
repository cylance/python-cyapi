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

    """ The following are duplicate methods from _Policies.py

    def add_scan_exclusions(self, exclusions, policy):
        for exclusion in exclusions:
            policy = self.append_policy_item('scan_exception_list', exclusion, policy)
        return policy

    def add_script_exclusions(self, exclusions, policy):
        if type(policy['script_control']['global_settings']['allowed_folders']) == str:
            policy['script_control']['global_settings']['allowed_folders'] = []
        if type(exclusions) == list:
            policy['script_control']['global_settings']['allowed_folders'] += exclusions
        else:
            policy['script_control']['global_settings']['allowed_folders'].append(exclusions)

        return policy

    def add_mem_exclusions(self, exclusions, policy):
        policy = self.append_mem_exclusion_items(exclusions, policy)
        return policy

    def add_template_exclusions(self, tpl_name, policy):

        f = pkg_resources.resource_stream('cyapi', "exclusions/{}.json".format(tpl_name))
        data = json.loads(f.read().decode('utf-8'))
        f.close()

        exclusions = data.get('memory',None)
        if exclusions is not None:
            policy = self.add_mem_exclusions(exclusions, policy)

        exclusions = data.get('protection', None)
        if exclusions is not None:
            policy = self.add_scan_exclusions(exclusions, policy)

        exclusions = data.get('script', None)
        if exclusions is not None:
            policy = self.add_script_exclusions(exclusions, policy)

        exclusions = data.get('trust_files_in_scan_exception_list', None)
        if exclusions is not None:
            if exclusions == True or exclusions == 1:
                policy = self.set_policy_item("trust_files_in_scan_exception_list", 1, policy)

        return policy

    def set_memdef(self, enabled, policy, mode="Alert"):

        if enabled == True:
            policy = self.set_policy_item('memory_exploit_detection',1,policy)
            policy = self.set_memdef_actions(policy, mode)
        elif enabled == False:
            policy = self.set_policy_item('memory_exploit_detection',0,policy)

        return policy

    def set_memdef_actions(self, policy, mode):
        for item in policy['memoryviolation_actions']['memory_violations']:
            item['action'] = mode

        for item in policy['memoryviolation_actions']['memory_violations_ext']:
            item['action'] = mode
        return policy

    def set_script_control(self, enabled, policy, mode="Alert", allowed_folders=None):

        if enabled == True:
            policy = self.set_policy_item('script_control',1,policy)
            policy = self.set_script_control_action(mode, mode,"Allow",mode,
                                               mode,allowed_folders,policy)
        elif enabled == False:
            policy = self.set_policy_item('script_control', 0, policy)

        return policy

    # TODO: Break this apart into individual functions
    def set_script_control_action(self,
                                  act_scr,
                                  macro,
                                  ps_console,
                                  ps_control,
                                  global_control,
                                  allowed_folders,
                                  policy):
        policy['script_control']["activescript_settings"]['control_mode'] = act_scr
        policy['script_control']["macro_settings"]['control_mode'] = macro
        policy['script_control']["powershell_settings"]['control_mode'] = ps_control
        policy['script_control']["powershell_settings"]['console_mode'] = ps_console


        policy['script_control']["global_settings"]['control_mode'] = global_control
        if allowed_folders is not None:
            policy['script_control']["global_settings"]['allowed_folders'] = allowed_folders
        return policy

    def enable_aqt(self, policy):
        policy = self.set_policy_item('auto_blocking', 1, policy)
        for item in policy['filetype_actions']['suspicious_files']:
            item['actions'] = 3
        for item in policy['filetype_actions']['threat_files']:
            item['actions'] = 3

        return policy

    def disable_btd(self, policy):
        return self.set_btd(0, policy)

    def enable_btd_once(self, policy):
        return self.set_btd(2, policy)

    def enable_btd_reocurring(self, policy):
        return self.set_btd(1, policy)

    def set_btd(self, val, policy):
        policy = self.set_policy_item('full_disc_scan', val, policy)
        return policy

    def disable_notifications(self, policy):
        policy = self.set_policy_item('show_notifications', "0", policy)
        return policy

    def enable_notifications(self, policy):
        policy = self.set_policy_item('show_notifications', "1", policy)
        return policy

    def enable_optics(self, policy):
        policy = self.set_policy_item('optics', 1, policy)
        return policy

    def set_policy_item(self, key, val, policy):
        for item in policy['policy']:
            if item['name'] == key:
                item['value'] = val
                return policy

    def get_policy_item(self, key, policy):
        for item in policy['policy']:
            if item['name'] == key:
                return item

    def append_policy_item(self, key, val, policy):
        for item in policy['policy']:
            if item['name'] == key:
                item['value'].append(val)
                return policy

    def append_mem_exclusion_items(self, items, policy):
        if type(items) == list:
            policy['memoryviolation_actions']['memory_exclusion_list'] += items
        else:
            policy['memoryviolation_actions']['memory_exclusion_list'].append(items)

        return policy """
