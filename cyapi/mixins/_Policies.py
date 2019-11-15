import json
import os
import pkg_resources

class Mixin:

    def delete_policies(self, policy_ids):
        """Delete multiple policies
        :param policy_ids: List of policy IDs to delete
        :return APIResponse
        """
        baseURL = self.baseURL + "policies/v2"

        if type(policy_ids) != list:
            raise TypeError("policy_ids must be a list type")

        data = {
            "tenant_policy_ids": policy_ids
        }

        return self._make_request("delete", baseURL, data=data)


    def get_policies(self, **kwargs):
        """Get a list of all Device Policies"""
        policies = self.get_list_items("policies", **kwargs)
        return policies

    def get_policy(self, policy_id):
        '''Get Policy Detail'''
        return self.get_item("policies", policy_id)

    def get_bulk_policy(self, policy_ids, disable_progress=True):
        """Get policy detail for many IDs
        :param policy_ids: list of policy_ids
        """
        baseURL = self.baseURL + "policies/v2/{}"
        urls = []
        if isinstance(policy_ids, list):
            for policy in policy_ids:
                urls.append(baseURL.format(policy))
            return self._bulk_get(urls, paginated=False, disable_progress=disable_progress)

    def delete_policy(self, policy_id):
        '''Delete policy by policy_id'''
        baseURL = self.baseURL + "policies/v2/{}".format(policy_id)

        return self._make_request("delete",baseURL)

    def create_device_policy(self, policy_name, policy_data=None):
        '''Success Code: 201'''
        baseURL = self.baseURL + "policies/v2"

        if policy_data is None:

            f = pkg_resources.resource_stream('cyapi', "reqs/create_policy.json")
            data = json.loads(f.read().decode('utf-8'))
            f.close()

        else:
            data = {'policy': policy_data}
            data['policy_id'] = ""
            data['policy']['checksum'] = ""
            data['policy']['policy_utctimestamp'] = ""

        data['user_id'] = self.app_id
        data['policy']['policy_name'] = policy_name
        response = self._make_request("post",baseURL, data=data)

        return response

    def update_policy(self, policy):
        '''Success Code: 204'''
        baseURL = self.baseURL + "policies/v2"

        policy['checksum'] = ""
        policy['policy_utctimestamp'] = ""

        request = {}
        request['user_id'] = self.app_id
        request['policy'] = policy

        return self._make_request("put",baseURL, data=request)

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

        return policy
