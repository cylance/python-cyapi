
class Mixin:

    def get_detections_by_severity(self, start=None, end=None, interval=None,
                                   detection_type=None, detected_on=None,
                                   event_number=None, device_name=None, status=None):
        """
        Returns the detections by severity
        :param start: Start Time in Zulu Format: 2019-09-13T00:00:00Z
        :param end: End Time in Zulu Format: 2019-09-15T23:59:59Z
        :param interval: Timer for grouping detections: Format: [0-9] + Time: 1y, 1M, 1d, 1h, 1m
        :param detection_type: DetectionDescription or DetectionName
        :param detected_on: Detected On time
        :param event_number: Phonetic ID
        :param device_name: Device Name Filter
        :param status: Filter on statuses: Values are New, In Progress, Follow Up, Reviewed, Done,
                       False Positive
        """
        # /detections/v2/severity?start={detection_start_timestamp}&end{detection_end_
        # timestamp}&interval={detection_interval}
        baseURL = self.baseURL + "detections/v2/severity"
        if not self._is_valid_detection_status(status):
            raise ValueError("Status Value not valid. Valid values: {}".format(
                                                                self.valid_detection_statuses))

        params = {
            "start": start,
            "end": end,
            "interval": interval,
            "detection_type": detection_type,
            "detected_on": detected_on,
            "event_number": event_number,
            "device": device_name,
            "status": status
        }
        baseURL = self._add_url_params(baseURL, params)
        return self._make_request("get",baseURL)

    def delete_detection(self, detection_id):
        """Deletes a detection
        :param detection_id: detection ID
        endpoint: /detections/v2/{detection_id}
        """

        baseURL = self.baseURL + "detections/v2/{}".format(detection_id)
        return self._make_request("delete",baseURL)

    def delete_detections(self, detection_ids):
        """Deletes a list of detections
        :param detection_ids: List of Detection IDs
        endpoint: /detections/v2/
        """
        baseURL = self.baseURL + "detections/v2/"
        data = { "ids": detection_ids }

        return self._make_request("delete",baseURL, data=data)

    # Get Detections
    def get_recent_detections(self, since, **kwargs):
        """Get Detections since a certain time
        :param since: Time in Zulu - Format: 2018-07-26T01:20:07.596Z
        """
        params = {"since": since}
        return self.get_list_items("detections", params=params, **kwargs)

    # Get Detections, might need better way to get additional detection pages
    def get_detections(self, zulu_start=None, zulu_end=None, severity=None,
                       detection_type=None, event_number=None, device_name=None,
                       status=None, sort=None, csv=False, **kwargs):
        ''':param start: Start time in Zulu: 2019-05-04T00:00:00.000Z
           :param end: End date-time in Zulu: 2019-05-04T23:00:00.000Z
           :param severity: Detection severity filter
             Values are Informational, Low, Medium, High.
           :param detection_type: Detection type filter
             Example: &detection_type=Powershell Download
           :param event_number: Event number filter - PhoneticId and DetectionID
           :param device: Device name filter
           :param status: The status for the detection event.
             Values are New, In Progress, Follow Up, Reviewed, Done, False Positive
           :param sort: Sort by the following fields
             (adding "-" in front of the value denotes descending order)
             * Severity
             * OccurrenceTime
             * Status
             * Device
             * PhoneticId
             * Description
             * ReceivedTime
        '''

        valid_sort = ["Severity", "OccurrenceTime","Status","Device","PhoneticId","Description","ReceivedTime"]
        valid_severity = ["Low", "Medium", "High"]

        if sort and sort not in valid_sort:
            raise ValueError("Sort Value not valid. Valid values: {}".format(valid_sort))

        if severity and severity not in valid_severity:
            raise ValueError("Severity Value not valid. Valid values: {}".format(valid_severity))

        if not self._is_valid_detection_status(status):
            raise ValueError("Status Value not valid. Valid values: {}".format(self.valid_detection_statuses))

        params = {"start": zulu_start,
                  "end": zulu_end,
                  "severity": severity,
                  "detection_type": detection_type,
                  "event_number": event_number,
                  "device": device_name,
                  "status": status,
                  "sort": sort}

        # If there are no values passed, the query will fail
        params = {k: v for k, v in params.items() if v is not None}

        if csv:
            baseURL = self.baseURL + "detections/v2/csv"
            baseURL = self._add_url_params(baseURL, params)
            return self._make_request("get", baseURL)

        return self.get_list_items("detections", params=params, **kwargs)


    # Get Detection, might need better way to get additional detection pages
    def get_detection(self, detection_id):
        """Get Detail about a detection
        :param detection_id: The detection ID or IDs to search for
        :example: detection_id=123 - This will return detail about one detection
        """
        baseURL = self.baseURL + "detections/v2/{}/details".format(detection_id)
        return self._make_request("get",baseURL)

    def get_bulk_detection(self, detection_ids, disable_progress=True):
        """Get detection detail for many IDs
        :param detection_ids: list of detection_ids
        """
        baseURL = self.baseURL + "detections/v2/{}/details"
        urls = []
        if isinstance(detection_ids, list):
            for detection in detection_ids:
                urls.append(baseURL.format(detection))
            return self._bulk_get(urls, paginated=False, disable_progress=disable_progress)


    def update_detection(self, detection_id, field, value):
      """
      :param detection_id: The Detection ID to update
      :param field: Field to update
      :param value: The data you'd like to update with
      endpoint: /detections/v2"""
      baseURL = self.baseURL + "detections/v2"

      valid_fields = ["comment", "status"]
      self._validate_parameters(field, valid_fields)

      if field == "status":
          self._is_valid_detection_status(value)

      data = [
              {
                "detection_id": detection_id,
                "field_to_update": { field: value }
              }
             ]

      return self._make_request("post",baseURL, data=data)
