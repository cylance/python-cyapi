
class Mixin:

    def get_package_execution(self, exec_id):
        # /packages/v2/executions/{unique_execution_id}
        baseURL = self.baseURL + "packages/v2/executions/{}".format(exec_id)
        return self._make_request("get",baseURL)

    def get_package_executions(self,exec_id):
        # /packages/v2/executions/{unique_execution_id}
        baseURL = self.baseURL + "packages/v2/executions/{}".format(exec_id)
        return self._make_request("get",baseURL)

    def delete_package_execution(self, exec_id):
        # /packages/v2/executions/{unique_execution_id}
        baseURL = self.baseURL + "packages/v2/executions/{}".format(exec_id)
        return self._make_request("delete",baseURL)

    def delete_package(self, package_id):
        # /packages/v2/{unique_package_id}
        baseURL = self.baseURL + "packages/v2/{}".format(package_id)
        return self._make_request("delete",baseURL)

    # Method to retrieve List of Packages
    def get_packages(self, **kwargs):

        return self.get_list_items("packages", **kwargs)

    # Method to execute a package by zone
    def execute_packages_by_zone(self, execution_name, zones, destination, arguments, package_to_execute, keepResultsLocally):
        baseURL = self.baseURL + "packages/v2/executions"

        data = {
            "execution": {
                "name": execution_name,
                "target": {
                    "zones": zones
                },
                "destination": destination,
                "packageExecutions": [
                    {
                        "arguments": arguments,
                        "package": package_to_execute
                    }
                ],
                "keepResultsLocally": keepResultsLocally
            }
        }

        return self._make_request("post",baseURL, data=data)

    def create_package(self, package_data):
        # /packages/v2
        baseURL = self.baseURL + "packages/v2"
        return self._make_request("post",baseURL, data=package_data)

    def create_package_execution(self, package_data):
        # /packages/v2/executions
        baseURL = self.baseURL + "packages/v2/executions"
        return self._make_request("post",baseURL, data=package_data)
