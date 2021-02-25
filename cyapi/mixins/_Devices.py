
class Mixin:

    def delete_devices(self, device_ids, callback_url=None):
        """Delete device(s) per ID(s)
        :param device_ids: must be a list of device_ids
        """
        baseURL = self.baseURL + "devices/v2"
        if callback_url == None:
            data = {
                "device_ids": device_ids
            }
            return self._make_request("delete", baseURL, data=data)
        else:
            data = {
                "device_ids": device_ids,
                "callback_url": callback_url
            }
            return self._make_request("delete", baseURL, data=data)

    def get_devices(self, **kwargs):
        '''Get a list of Devices'''
        return self.get_list_items('devices', **kwargs)

    def get_devices_extended(self, **kwargs):
        '''Get a list of Devices w/ extended information'''
        return self.get_list_items('devices', detail='/extended', **kwargs)

    def get_device_count(self, **kwargs):
        '''Get a list of list of products, product versions,
        and number of devices using a product and product version
        '''
        return self.get_item('devices', 'products')

    def get_device(self, device_id):
        '''Get Device Detail'''
        return self.get_item("devices", device_id)

    def get_bulk_device(self, device_ids, disable_progress=True):
        """Get device detail for many IDs
        :param device_ids: list of device_ids
        """
        baseURL = self.baseURL + "devices/v2/{}"
        urls = []
        if isinstance(device_ids, list):
            for device in device_ids:
                urls.append(baseURL.format(device))
            return self._bulk_get(urls, paginated=False, disable_progress=disable_progress)

    def get_device_by_mac(self, mac):
        '''Get Device Detail by MAC Address'''

        return self.get_item("devices", "macaddress/{}".format(mac))

    def get_device_threats(self, device_id, **kwargs):
        # /devices/v2/{unique_device_id}/threats?page=m&page_size=n
        detail = "/{}/threats".format(device_id)

        return self.get_list_items("devices", detail=detail, **kwargs)

    def get_zone_devices(self, zone_id, **kwargs):
        '''Return list of devices for a given zone'''
        #/devices/v2/{unique_zone_id}/devices?page=m&page_size=n

        detail = "/" + zone_id + "/devices"
        return self.get_list_items("devices", detail=detail, **kwargs)

    def update_device(self, device_id, device):
        """endpoint: /devices/v2/{unique_device_id}"""
        baseURL = self.baseURL + "devices/v2/{}".format(device_id)
        return self._make_request("put",baseURL, data=device)

    def update_device_threat(self, device_id, event, threat_id):
        """endpoint: /devices/v2/{unique_device_id}/threats"""
        baseURL = self.baseURL + "devices/v2/{}/threats".format(device_id)
        valid_events = ["Quarantine", "Waive"]
        self._validate_parameters(event, valid_events)
        data = {"threat_id": threat_id, "event":event}
        return self._make_request("post",baseURL, data=data)

    def get_agent_installer_link(self, product, os, arch, package, build=None):
        """endpoint: /devices/v2/installer?product=p&os=o&package=k&architecture=a&build=v"""
        baseURL = self.baseURL + "devices/v2/installer"
        valid_products = ["Protect", "Optics", "Protect Optics"]
        valid_packages = ["Exe", "Msi", "Dmg", "Pkg", ""]
        valid_archs = ["X86", "X64", "AmazonLinux1", "AmazonLinux2", "CentOS6", "CentOS6UI",
                       "CentOS7", "CentOS7UI", "Ubuntu1404", "Ubuntu1404UI", "Ubuntu1604",
                       "Ubuntu1604UI", "Ubuntu1804", "Ubuntu1804UI" ]
        valid_os = [ "AmazonLinux1", "AmazonLinux2", "CentOS7", "Linux", "Mac", "Ubuntu1404",
                     "Ubuntu1604", "Ubuntu1804", "Windows" ]

        self._validate_parameters(product, valid_products)
        self._validate_parameters(os, valid_os)
        self._validate_parameters(package, valid_packages)
        self._validate_parameters(arch, valid_archs)
        params = {"product": product, "os": os, "architecture": arch, "package": package, "build": build}
        baseURL = self._add_url_params(baseURL, params)

        return self._make_request("get",baseURL)
