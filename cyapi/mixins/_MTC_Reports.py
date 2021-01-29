
class Mixin:

    def get_mtc_report_runs(self, **kwargs):
        """Get a list of all MTC Report Runs
        Returns: listData: [ReportRuns], totalCount
        """
        baseURL = self.baseURL + "reports/report-runs"
        return self._make_request("get",baseURL)

    def get_mtc_report(self, report_run_id):
        """Delete MTC Device Policy Template by policy_template_id"""
        baseURL = self.baseURL + "reports/report-runs/{}/download".format(report_run_id)
        return self._make_request("get",baseURL)

    def get_mtc_reports(self, **kwargs):
        """Get a list of all MTC Reports
        Returns: listData: [Reports], totalCount
        """
        baseURL = self.baseURL + "reports/list"
        return self._make_request("get",baseURL)

    def run_mtc_report(self, report_run_id):
        """Delete MTC Device Policy Template by policy_template_id"""
        baseURL = self.baseURL + "reports/report-runs/{}/download".format(report_run_id)
        return self._make_request("post", baseURL)