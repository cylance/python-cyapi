
class Mixin:


    def resend_mtc_invite_email(self, user_id):
        """Resend MTC user invitation
        Params: user_id
        """
        baseURL = self.baseURL + "users/{}/resend-invite".format(user_id)

        return self._make_request("post",baseURL)

    def create_mtc_user(self, email, first, last, roleNames=["Partner Administrator"]):
        """Create MTC User
        Params: email, First, Last, roleNames[]
        """

        data = {
                "first_name": first,
                "last_name": last,
                "roleName": roleNames,
                "email": email
        }

        baseURL = self.baseURL + "users"
        return self._make_request("post",baseURL, data=data)

    def update_mtc_user(self, user_id, user_obj):
        """Update a MTC User
        Params: user_id, user_obj
        """
        baseURL = self.baseURL + "users/{}".format(user_id)
        return self._make_request("put",baseURL, data=user_obj)

    def delete_mtc_user(self, uid):
        """Delete MTC User"""
        baseURL = self.baseURL + "users/{}".format(uid)
        return self._make_request("delete",baseURL)

    def get_mtc_users(self, **kwargs):
        """Get MTC Users
        Returns: listData: [Users], totalCount
        """
        baseURL = self.baseURL + "users/list"
        return self._make_request("get",baseURL)



