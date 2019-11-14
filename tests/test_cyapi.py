import unittest
import argparse
from pprint import pprint
import json
import sys
import logging
from cyapi.cyapi import CyAPI

class CyAPITest(unittest.TestCase):
    tid = None
    app_id = None
    app_secret = None
    region = "NA"

    @classmethod
    def setUpClass(cls):
        cls.API = CyAPI(cls.tid, cls.app_id, cls.app_secret, cls.region)
        cls.log = logging.getLogger("TestLog")

    def test_conn(self):
        self.API.create_conn()
        assert(self.API.jwt is not None)

### unittest Utility Functions ###
    def does_policy_name_exist(self, name):
        policies = self.API.get_policies()
        for p in policies.data:
            if name == p['name']:
                return True
        return False

    def get_policy_by_name(self, name):
        policies = self.API.get_policies()
        for p in policies.data:
            if name == p['name']:
                return p
        return False

    def get_user_by_email(self, email):
        users = self.API.get_users()
        for p in users.data:
            if email == p['email']:
                self.log.debug("  [+] Found existing User")
                return p
        return False

    def clean_test_user(self, email):
        user = self.get_user_by_email(email)
        if not user:
            return True
        else:
            response = self.API.delete_user(user['id'])
            if response.is_success:
                return True
            else:
                return False

### User API ###

    # TODO: Fix this test
    # def test_create_user(self):
    #     self.log.debug('  [+] test_create_user')
    #     email = 'testuser@email.com'
    #     if not self.clean_test_user(email):
    #         self.log.debug('  [+] create_user clean existing user failed')
    #     else:
    #         self.log.debug('  [+] create_user clean existing user success')
    #     response = self.API.create_user(email, 'Test', 'User')
    #     self.log.debug(response.errors)
    #     self.log.debug(response.data)
    #     assert(response.is_success)
    #     self.clean_test_user(email)

    def test_get_users(self):
        response = self.API.get_users()
        assert( isinstance(response.data, list) )

    def test_get_user(self):
        response = self.API.get_users()
        user = self.API.get_user(response.data[0]["id"])
        assert(isinstance(user.data, dict))

    # TODO: Fix this test
    # def test_update_user(self):
    #     #TODO: No idea why this is failing validation.
    #     email = 'testuser@email.com'
    #     response = self.API.create_user(email, 'Test', 'User')
    #     user = self.get_user_by_email(email)
    #     user_id = user['id']
    #     updated_user = {
    #                     'email' : 'updateduser@email.com',
    #                     'user_role' : '00000000-0000-0000-0000-000000000002',
    #                     'first_name' : 'Updated',
    #                     'last_name' : 'User',
    #                     'zones' : []
    #                     }
    #     pprint(user)
    #     print()
    #     pprint(updated_user)
    #     response = self.API.update_user(user_id, user)
    #     print(response.status_code)
    #     pprint(response.errors)
    #     pprint(response.data)
    #     assert(response.is_success)
    #     #self.clean_test_user(email)

    # TODO: Fix this test
    # def test_delete_user(self):
    #     self.log.debug('  [+] test_delete_user')
    #     email = 'testuser@email.com'
    #     user = self.get_user_by_email(email)
    #     if not user:
    #         response = self.API.create_user(email, 'Test', 'User')
    #         if response.is_success:
    #             user = self.get_user_by_email(email)
    #         else:
    #             self.log.debug('  [+] Failed to find created user by email')
    #     response = self.API.delete_user(user['id'])
    #     assert(response.is_success)

    def test_send_invite_email(self):
        email = 'testuser@email.com'
        response = self.API.create_user(email, 'Test', 'User')
        if response.is_success:
            sent = self.API.send_invite_email(response.data["email"])
            assert(sent.is_success)
        else:
            self.log.debug(response.status_code)
        self.clean_test_user(email)

    def test_send_request_password_email(self):
        email = 'testuser@email.com'
        response = self.API.create_user(email, 'Test', 'User')
        if response.is_success:
            sent = self.API.send_invite_email(response.data["email"])
            assert(sent.is_success)
        else:
            self.log.debug(response.status_code)
        self.clean_test_user(email)

### Devices API ###
    def test_get_devices(self):
        response = self.API.get_devices()
        assert( response.is_success )

    def test_get_device(self):
        response = self.API.get_devices()
        dev = response.data[0]
        dev_detail = self.API.get_device(dev["id"])
        assert( isinstance(dev_detail.data, dict) )

    def test_get_device_by_mac(self):
		# short for test_get_device_by_mac_address
        response = self.API.get_devices()
        devs = self.API.get_device_by_mac(response.data[0]["mac_addresses"][0])
        assert(len(devs.data) > 0)

    @unittest.skip('Test Not Implemented')
    def test_update_device(self):
        raise NotImplementedError

    @unittest.skip('Test Not Implemented')
    def test_get_device_threat(self):
        raise NotImplementedError

    @unittest.skip('Test Not Implemented')
    def test_update_device_threat(self):
        raise NotImplementedError

    def test_get_zone_devices(self):
        pass
        # These responses that are only lists need a better test, but when they are empty due to tenant
        # then what? This works, just not sure when it is a false possative.
        #zoneId = "Create Method to pull valid ZoneId"
        """ response = self.API.get_zones()
        self.log.debug("Validate devices in zone: {}".format(response[0]["name"]))
        #assert(len(self.API.get_zone_devices(response[0]["id"])) > 0)
        response = self.API.get_zone_devices(zoneId)
        assert(response.status_code == 200)"""

    @unittest.skip('Test Not Implemented')
    def test_get_agent_installer_link(self):
        raise NotImplementedError

    @unittest.skip('Test Not Implemented')
    def test_delete_devices(self):
        raise NotImplementedError

### Global List API ###
    def test_get_global_list(self):
        lists = ["quarantine", "safe"]
        for l in lists:
            response = self.API.get_global_list( l )
            assert( isinstance(response.data, list) )
            #assert(response.status_code == 200)

    @unittest.skip('Test Not Implemented')
    def test_add_to_global_list(self):
        raise NotImplementedError

    @unittest.skip('Test Not Implemented')
    def test_delete_from_global_list(self):
        raise NotImplementedError

### Zone API ###
    def test_get_zones(self):
        response = self.API.get_zones()
        assert( response.is_success )

    @unittest.skip('Test Not Implemented')
    def test_delete_zones(self):
        pass

### Policy API ###
# create policy, configure policy, apply policy, validate that it works
    def test_create_policy(self, name="PyUnitTest - Create Policy"):
        # We need to 'undo' everything we do during testing. This will remove/delete the policy we create
        self.addCleanup(self.delete_policy_by_name, name)
        policyExists = self.get_policy_by_name(name)
        if type(policyExists) == bool:
            response = self.API.create_device_policy(name)
            self.log.debug(response.status_code)
            assert(response.status_code == 201)
        else:
            self.log.debug("Deleting test policy: {}".format(name))
            response = self.API.delete_policy(policyExists['id'])
            self.log.debug(response.status_code)
            response = self.API.create_device_policy(name)
            self.log.debug(response.status_code)
            assert(response.status_code == 201)

    def test_get_policies(self):
        # This works because even a new tenant has a policy
        response = self.API.get_policies()
        assert(len(response.data) > 0)

    def test_delete_policy(self, name="PyUnitTest - Delete Policy"):
        policyExists = self.get_policy_by_name(name)
        print()
        if not policyExists:
            print("Creating new Policy")
            response = self.API.create_device_policy(name)
            response = response.data
        else:
            print("Got existing policy")
            response = policyExists

        if isinstance(response, dict):
            name = response.get('name') if response.get('name') else response.get('policy_name')
            policy_id = response.get('id') if response.get('id') else response.get('policy_id')
            self.log.debug("Deleting test policy: {}".format(name))
            self.log.debug("Test policy ID: {}".format(policy_id))

        response = self.API.delete_policy(policy_id)
        """ {'date_added': '2019-10-31T17:27:23.6470751',
            'date_modified': '2019-10-31T17:27:23.6470751',
            'device_count': 0,
            'id': '6daf8a99-d47e-47f9-b269-8c6431f1aa6d',
            'name': 'PyUnitTest - Delete Policy',
            'zone_count': 0} """
        # pprint(response.data)
        assert(response.is_success)

    """ def test_policy_configuration(self):
        name = "PyUnitTest - Policy"
        self.addCleanup(self.API.delete_policy, name) """

    def test_policy(self):
        name = "PyUnitTest - Test Policy"

        # We need to 'undo' everythign we do during testing. This will remove/delete the policy we create
        self.addCleanup(self.delete_policy_by_name, name)
        policyExists = self.get_policy_by_name(name)
        if type(policyExists) == bool:
            response = self.API.create_device_policy(name)
        else:
            response = policyExists
        #response = self.API.create_device_policy(name)
        self.log.debug(response.status_code)
        if isinstance(response.data, list):
            assert( isinstance(response.data, list) )
        else:
            assert(response.status_code == 201)
        walk_policy = response.data

        walk_policy = self.API.enable_aqt(walk_policy)
        walk_policy = self.API.disable_btd(walk_policy)
        walk_policy = self.API.enable_optics(walk_policy)
        walk_policy = self.API.set_memdef(True, walk_policy, "Alert")
        walk_policy = self.API.set_script_control(True, walk_policy)

        self.log.debug("[+] Updating Policy: {}".format(name))
        response = self.API.update_policy(walk_policy)
        # Test to make sure the update succeeded
        assert(response.status_code == 204)
        policy = self.API.get_policy(walk_policy['policy_id'])

        item = self.API.get_policy_item('auto_blocking',policy.data)
        self.assertEqual(item['value'], '1')

    # Utility Functions

    @unittest.skip('Test Not Implemented')
    def exc_choices(self):
        raise NotImplementedError

    @unittest.skip('Test Not Implemented')
    def regions(self):
        raise NotImplementedError


    def delete_policy_by_name(self, name):
        policyExists = self.get_policy_by_name(name)
        if type(policyExists) == bool:
            response = self.API.create_device_policy(name)
            response = response.data
        else:
            response = policyExists
        #item = response.data
        #pprint(response)
        self.log.debug("Deleting policy by name: {}".format(response['name']))
        self.log.debug("Test policy ID: {}".format(response['id']))
        response = self.API.delete_policy(response['id'])
        if response.status_code == 204:
            return True
        else:
            return False


### Missing Tests by API ###

### User API ###

### Device API ###

### Global List API ###

### Policy API ###

    @unittest.skip('Test Not Implemented')
    def test_delete_policies(self):
        pass


### Zone API ###
    @unittest.skip('Test Not Implemented')
    def test_get_device_zones(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_update_zone(self):
        pass


### Threat API ###
    def test_get_threats(self):

        threats = self.API.get_threats()
        assert(isinstance(threats.data, list))

    def test_get_threat(self):
        threats = self.API.get_threats()
        threat = self.API.get_threat(threats.data[0]['sha256'])
        assert(threats.data[0]['sha256'] == threat.data['sha256'])

    def test_get_threat_devices(self):
        threats = self.API.get_threats()
        threat_devices = self.API.get_threat_devices(threats.data[0]['sha256'])
        assert( len(threat_devices.data) > 0 )

    @unittest.skip('Test Not Implemented')
    def test_get_threat_download_url(self):
        pass


### Detection API ###
    def test_get_detections(self):
        ## Add tests to test optional query string parameters
        response = self.API.get_detections()
        assert( isinstance(response.data, list) )

        response = self.API.get_detections(csv=True)
        assert( isinstance(response.data, str) )


    @unittest.skip('Test Not Implemented')
    def test_get_recent_detections(self):
        # Need recent date function that outputs UTC
        response = self.API.get_recent_detections(since='00000Z')
        assert( isinstance(response, list) )
        #assert(response.status_code == 200)

    @unittest.skip('Test Not Implemented')
    def test_get_detections_by_severity(self):
        #/severity?start={detection_start_timestamp}&end{detection_end_ timestamp}&interval={detection_interval}
        # Needs UTC Dates and maybe an interval List
        pass

    @unittest.skip('Test Not Implemented')
    def test_update_detection(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_delete_detection(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_delete_detections(self):
        pass


### Package Deployment API ###
    @unittest.skip('Test Not Implemented')
    def test_create_package(self):
        pass

    def test_get_packages(self):
        response = self.API.get_packages()
        assert( isinstance(response.data, list) )
        #assert(response.status_code == 200)

    @unittest.skip('Test Not Implemented')
    def test_delete_package(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_create_package_execution(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_get_package_executions(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_delete_package_execution(self):
        pass


### Detection Rule API ###
    def test_get_detection_rules(self):
        response = self.API.get_detection_rules()
        assert( isinstance(response.data, list) )
        #assert(response.status_code == 200)
        response = self.API.get_detection_rules(True)
        #assert( isinstance(response.data, dict) )
        assert(response.status_code == 200)

    def test_get_detection_rule(self):
        ruleId = 'MAKE PROCESS TO GET ONE'
        response = self.API.get_detection_rule(ruleId)

        # assert( isinstance(response.data, dict) )
        # #assert(response.status_code == 200)
        # response = self.API.get_detection_rule(ruleId, natlang=True)
        # assert( isinstance(response.data, list) )
        # #assert(response.status_code == 200)

    """ #Sent as Argument to get_detection_rule
    def test_get_detection_rule_csv(self):
        response = self.API.get_detection_rule_csv()
        assert(response.status_code == 200) """

    @unittest.skip('Test Not Implemented')
    def test_validate_detection_rule(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_create_detection_rule(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_update_detection_rule(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_deactivate_or_delete_detection_rule(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_get_detection_rule_counts(self):
        pass

### Detection Rule Sets ###
    @unittest.skip('Test Not Implemented')
    def test_get_detection_rule_set(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_create_detection_rule_set(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_retrieve_default_detection_rule_set_update_detection_rule_set(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_delete_detection_rule_set(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_delete_multiple_detection_rule_sets(self):
        pass

### Detection Exceptions ###
    def test_get_detection_exceptions(self):
        response = self.API.get_detection_exceptions()
        # pprint(response.data)
        assert( isinstance(response.data, list) )
        #assert(response.status_code == 200)
        response = self.API.get_detection_exceptions(True)
        #assert( isinstance(response.data, list) )
        assert(response.status_code == 200)

    @unittest.skip('Test Not Implemented')
    def test_get_detection_exception_content(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_create_detection_exception(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_update_detection_exception(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_deactivate_delete_detection_exception(self):
        pass

### Device Commands ###
    @unittest.skip('Test Not Implemented')
    def test_lockdown_device_command(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_get_device_lockdown_history(self):
        pass

    def test_get_retrieved_file_results(self):
        response = self.API.get_retrieved_file_results()
        assert( isinstance(response.data, list) )
        #assert(response.status_code == 200)

    @unittest.skip('Test Not Implemented')
    def test_request_file_retrieval_from_device(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_check_file_retrieval_status_from_device(self):
        pass

### Focus View ###
    def test_get_focus_views(self):
        response = self.API.get_focus_views()
        assert( isinstance(response.data, list) )
        #assert(response.status_code == 200)

    @unittest.skip('Test Not Implemented')
    def test_search_for_focus_view_results(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_request_a_focus_view(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_get_a_focus_view_summary(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_get_focus_view_results(self):
        pass

### InstaQueries ###
    def test_get_instaqueries(self):
        response = self.API.get_instaqueries()
        assert( isinstance(response.data, list) )
        #assert(response.status_code == 200)

    @unittest.skip('Test Not Implemented')
    def test_create_instaquery(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_get_instaquery(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_get_instaquery_results(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_archive_instaquery(self):
        pass

### cylanceOPTICS Policy ###
    def test_get_rule_sets_to_policy_mapping(self):
        response = self.API.get_rule_sets_to_policy_mapping()
        assert( isinstance(response.data, list) )
        #assert(response.status_code == 200)

    @unittest.skip('Test Not Implemented')
    def test_get_detection_rule_set_for_a_policy(self):
        pass

    @unittest.skip('Test Not Implemented')
    def test_update_a_detection_rule_set_in_a_policy(self):
        pass




def ParseArgs():

    regions = []
    regions_help =  "Region the tenant is located: "
    for (k, v) in CyAPI.regions.items():
        regions.append(k)
        regions_help += " {} - {} ".format(k,v['fullname'])

    parser = argparse.ArgumentParser(description='Create a new OPTICS Rule Set based on an existing on and best practice phases.', add_help=True)
    parser.add_argument('-v', '--verbose', action="count", default=0, dest="verbose",
                        help='Show process location, comments and api responses')
    parser.add_argument('-f', '--failfast', dest='failfast', help="Tests should fail immediately", action='store_true', default=False)
    # Cylance SE Tenant
    parser.add_argument('-tid', '--tid_val', help='Tenant Unique Identifier')
    parser.add_argument('-aid', '--app_id', help='Application Unique Identifier')
    parser.add_argument('-ase', '--app_secret', help='Application Secret')
    parser.add_argument('-c', '--creds_file', dest='creds', help='Path to JSON File with self.API info provided')
    parser.add_argument('-r', '--region', dest='region', help=regions_help, choices=regions, default='NA')

    return parser

if __name__ == '__main__':

    commandline = ParseArgs()
    args = commandline.parse_args()
    if args.verbose >= 1:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    if args.creds:
        with open(args.creds, 'rb') as f:
            creds = json.loads(f.read())
        tid_val = creds['tid']  # The tenant's unique identifier.
        app_id = creds['app_id']      # The application's unique identifier.
        app_secret = creds['app_secret'] # The application's secret to sign the auth token with.

    elif args.tid_val and args.app_id and args.app_secret:
        tid_val = args.tid_val
        app_id = args.app_id
        app_secret = args.app_secret

    else:
        print("[-] Must provide valid token information")
        exit(-1)

    CyAPITest.tid = tid_val
    CyAPITest.app_id = app_id
    CyAPITest.app_secret = app_secret
    CyAPITest.region = args.region

    sys.argv = sys.argv[:1]

    unittest.main(failfast=args.failfast)

