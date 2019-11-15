
class Mixin:

    def create_zone(self, name, policy):
        '''Create a zone and assign policy'''
        data = {
                "name": name,
                "policy_id": policy['policy_id'],
                "criticality": "Normal"
               }

        return self.create_item("zones", data)

    def delete_zone(self, zone_id):
        '''Delete zone by zone_id'''
        baseURL = self.baseURL + "zones/v2/{}".format(zone_id)

        return self._make_request("delete",baseURL)

    def get_zones(self, **kwargs):
        zones = self.get_list_items("zones", **kwargs)
        return zones

    def get_zone(self, zone_id):
        '''Get Policy Detail'''
        return self.get_item("zones", zone_id)

    def get_bulk_zone(self, zone_ids, disable_progress=True):
        """Get zone detail for many IDs
        :param zone_ids: list of zone_ids
        """
        baseURL = self.baseURL + "zones/v2/{}"
        urls = []
        if isinstance(zone_ids, list):
            for zone in zone_ids:
                urls.append(baseURL.format(zone))
            return self._bulk_get(urls, paginated=False, disable_progress=disable_progress)

    def get_device_zones(self, device_id, **kwargs):
        detail = "/{}/zones".format(device_id)
        return self.get_list_items("zones", detail, **kwargs)

    def update_zone(self, zone_id, name, policy_id, criticality):
        # /zones/v2/{unique_zone_id}
        baseURL = self.baseURL + "zones/v2/{}".format(zone_id)

        data = {
                "name": name,
                "policy_id": policy_id,
                "criticality": criticality
            }
        return self._make_request("put",baseURL, data=data)
