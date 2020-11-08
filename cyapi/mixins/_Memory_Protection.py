class Mixin:

    def get_memory_protection_events(self, start_time=None, end_time=None, **kwargs):
        '''Get a list of Memoryprotection Events'''
        if end_time and not start_time:
            raise ValueError("start_time must be set if using end_time parameter")
        params = {"start_time": start_time, "end_time": end_time}

        return self.get_list_items('memoryprotection', params=params, **kwargs)


    def get_memory_protection_event(self, device_image_file_event_id):
        '''Get Memoryprotection Detail'''
        return self.get_item("memoryprotection", device_image_file_event_id)

