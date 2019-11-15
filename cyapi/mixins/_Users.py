
class Mixin:

    def delete_user(self, uid):
        baseURL = self.baseURL + "users/v2/{}".format(uid)

        return self._make_request("delete",baseURL)

    def send_invite_email(self, email):
        baseURL = self.baseURL + "users/v2/{}/invite".format(email)

        return self._make_request("post",baseURL)

    #def send_request_password_email(self):
    def send_password_reset_email(self, email):
        baseURL = self.baseURL + "users/v2/{}/resetpassword".format(email)

        return self._make_request("post",baseURL)

    def get_users(self, **kwargs):
        return self.get_list_items('users', **kwargs)

    def get_user(self, user_id):
        return self.get_item("users", user_id)

    def create_user(self, email, first, last, user_role="Administrator", zones=[]):
        """
        endpoint: /users/v2
        zones: parameter Example -
        "zones": [
                    {
                    "id": "d27ff5c4-5c0d-4f56-a00d-a1fb297e440e",
                    "role_type": "00000000-0000-0000-0000-000000000002"
                    }
                ]
        """

        roles = {
            "User": "00000000-0000-0000-0000-000000000001",
            "Administrator": "00000000-0000-0000-0000-000000000002",
            "Zone Manager": "00000000-0000-0000-0000-000000000003"
        }
        self._validate_parameters(user_role, roles.keys())

        data = {
                "email": email,
                "user_role": roles[user_role],
                "first_name": first,
                "last_name": last,
                "zones": zones
        }

        if not zones or user_role == "Administrator":
            data.pop("zones")

        baseURL = self.baseURL + "users/v2"
        return self._make_request("post",baseURL, data=data)

    def update_user(self, user_id, user_obj):
        """endpoint: /users/v2/{user_id}"""

        baseURL = self.baseURL + "users/v2/{}".format(user_id)

        return self._make_request("put",baseURL, data=user_obj)
