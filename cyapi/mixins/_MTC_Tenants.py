
class Mixin:
    '''TODO: Test Policy and
    create provision, update, get install-token, regen install-token
    '''

    def get_tenant_app(self, venueTenantId):
        """Get MTC Tenant's Bearer Token
        The Bearer JWT is returned as a string in APIRequest.data
        """
        baseURL = self.baseURL + "tenants/tenant-app/{}".format(venueTenantId)
        return self._make_request("put", baseURL)

    def apply_policy(self, venueTenantIds, policyTemplateId):
        """
        Applies a policy template to a group of tenants. Max of 50 tenants can be in the request.
        venueTenantIds is a list object.
        """
        print("In apply_policy")

        data = {
                "venueTenantIds": venueTenantIds,
                "policyTemplateId": policyTemplateId
        }

        return self._make_request("post",baseURL, data=data)

    def get_tenants(self, **kwargs):
        return self.get_item("tenants", "list", **kwargs)

