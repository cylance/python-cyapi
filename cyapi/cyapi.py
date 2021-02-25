# cyAPI.py is designed to have reusable methods and classes for the Cylance v2 API
# python 2.x & 3.x tested

##################################################################################
# USAGE
##################################################################################

import glob
import json
import os
import re
import time
import uuid
from datetime import datetime, timedelta
from pprint import pprint
from random import shuffle

import jwt  # PyJWT version 1.5.3 as of the time of authoring.
import pkg_resources
import requests  # requests version 2.18.4 as of the time of authoring.
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm
import concurrent.futures as cf

from .mixins._Detections import Mixin as DetectionsMixin
from .mixins._DeviceCommands import Mixin as DeviceCommandsMixin
from .mixins._Devices import Mixin as DevicesMixin
from .mixins._Exceptions import Mixin as ExceptionsMixin
from .mixins._Focus_View import Mixin as FocusViewMixin
from .mixins._Global_List import Mixin as GlobalListMixin
from .mixins._InstaQueries import Mixin as InstaQueriesMixin
from .mixins._Memory_Protection import Mixin as MemoryProtectionMixin
from .mixins._Optics_Policies import Mixin as OpticsPoliciesMixin
from .mixins._Packages import Mixin as PackagesMixin
from .mixins._Policies import Mixin as PoliciesMixin
from .mixins._Rules import Mixin as RulesMixin
from .mixins._Rulesets import Mixin as RulesetMixin
from .mixins._Threats import Mixin as ThreatsMixin
from .mixins._Users import Mixin as UsersMixin
from .mixins._Zones import Mixin as ZonesMixin
from .mixins._MTC_HealthCheck import Mixin as MTCHealthCheckMixin
from .mixins._MTC_PolicyTemplates import Mixin as MTCPolicyTemplatesMixin
from .mixins._MTC_Reports import Mixin as MTCReportsMixin
from .mixins._MTC_Tenants import Mixin as MTCTenantsMixin
from .mixins._MTC_Users import Mixin as MTCUsersMixin

try:
    from urllib import urlencode, unquote
    from urlparse import urlparse, parse_qsl, ParseResult
except ImportError:
    # Python 3 fallback
    from urllib.parse import (
        urlencode, unquote, urlparse, parse_qsl, ParseResult
    )


class CyAPI(DetectionsMixin,DevicesMixin,DeviceCommandsMixin,ExceptionsMixin,
            FocusViewMixin, GlobalListMixin,InstaQueriesMixin,MemoryProtectionMixin,OpticsPoliciesMixin,
            PackagesMixin,PoliciesMixin,RulesMixin,RulesetMixin,
            ThreatsMixin,UsersMixin,ZonesMixin,MTCHealthCheckMixin,MTCPolicyTemplatesMixin,
            MTCReportsMixin,MTCTenantsMixin,MTCUsersMixin):
    """The main class that should be used. Each of the Mixins above provides the
       functionality for that specific API. Example: DetectionsMixin implements
       all relevant functions to getting / working with detections.

       Example Usage:
         API = CyAPI(tid="your_tid", app_id="your_app_id", app_secret="your_secret")
         API.create_conn()
       At this point you're ready to begin interacting with the API.
    """
    regions = {
       'NA': {'fullname': 'North America',       'url':''},
       'US': {'fullname': 'United States',                          'mtc_url':'us'},
       'APN': {'fullname': 'Asia Pacific-North', 'url': '-apne1'},
       'JP': {'fullname': 'Asia Pacific NE/Japan',                  'mtc_url':'jp'},
       'APS': {'fullname': 'Asia Pacific-South', 'url': '-au'},
       'AU': {'fullname': 'Asia Pacific SE/Australia',              'mtc_url':'au'},
       'EU': {'fullname': 'Europe',              'url': '-euc1',    'mtc_url':'eu'},
       'GOV': {'fullname': 'US-Government',      'url': '-us'},
       'SA': {'fullname': 'South America',       'url': '-sae1'},
       'SP': {'fullname': 'South America/Sao Paulo',                'mtc_url': 'sp'}
    }

    valid_detection_statuses = ["New", "In Progress", "Follow Up", "Reviewed", "Done", "False Positive"]
    valid_artifact_types = ["Protect", "Process", "File", "NetworkConnection", "RegistryKey"]

    root_path = os.path.dirname(os.path.abspath(__file__))

    exclusions = pkg_resources.resource_listdir(__name__, "exclusions")

    exc_choices = list(map(lambda x: os.path.basename(x).replace('.json',''), exclusions))

    WORKERS = 20

    def __init__(self, tid=None, app_id=None, app_secret=None, region="NA", mtc=False, tenant_app=False, tenant_jwt=None):
        self.tid_val = tid
        self.app_id = app_id
        self.app_secret = app_secret
        self.jwt = None
        self.region = region
        self.mtc = mtc
        self.tenant_app = tenant_app
        self.tenant_jwt = tenant_jwt

        if self.mtc:
            self.baseURL = "https://api-admin.cylance.com/public/{}/".format(self.regions[region]['mtc_url'])
        else:
            self.baseURL = "https://protectapi{}.cylance.com/".format(self.regions[region]['url'])
        self.debug_level = debug_level
        self.s = None
        self.req_cnt = 0

    def create_conn(self):
        """
        Setup and authenticate the connection to the API
        """

        self.s = self._setup_session(session=self.s)

        if self.mtc:
            self.auth = self._get_auth_token()
            self.headers = {
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "*/*",
                'Accept-Encoding': "gzip,deflate,br",
                'Authorization': "Bearer {}".format(self.auth)
            }
        else:
            if self.tenant_app:
                self.jwt = self.tenant_jwt
            else:
                self.jwt = self._get_jwt()
            self.headers = {
                'Accept': "application/json",
                'Accept-Encoding': "gzip,compress",
                'Authorization': "Bearer {}".format(self.jwt),
                'Cache-Control': "no-cache"
            }

        # # 30 minutes from now
        timeout = 1800
        now = datetime.utcnow()
        timeout_datetime = now + timedelta(seconds=timeout)
        self.access_token_expiration = timeout_datetime - timedelta(seconds=30)

        self.s.headers.update(self.headers)

    def _setup_session(self, retries=250, backoff_factor=0.8,
        backoff_max=180, status_forcelist=(500, 502, 503, 504),
        session=None):
        """Creates a session with a Retry handler. This will automatically retry
           up to 250 times... which might be overkill
        """

        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount(self.baseURL, adapter)
        return session

    def _get_jwt(self):
        '''Create a JWT that expires in 30min'''
        # 30 minutes from now
        timeout = 1800
        now = datetime.utcnow()
        timeout_datetime = now + timedelta(seconds=timeout)
        epoch_time = int((now - datetime(1970, 1, 1)).total_seconds())
        epoch_timeout = int((timeout_datetime - datetime(1970, 1, 1)).total_seconds())
        jti_val = str(uuid.uuid4())

        AUTH_URL = self.baseURL + "auth/v2/token"
        claims = {
            "exp": epoch_timeout,
            "iat": epoch_time,
            "iss": "http://cylance.com",
            "sub": self.app_id,
            "tid": self.tid_val,
            "jti": jti_val
        }

        encoded = jwt.encode(claims, self.app_secret, algorithm='HS256').decode('utf-8')
        if debug_level > 2:
            print( "auth_token:\n" + encoded + "\n" )
        payload = {"auth_token": encoded}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        resp = requests.post(AUTH_URL, headers=headers, data=json.dumps(payload))

        # Can't do anything without a successful authentication
        try:
            assert resp.status_code == 200
        except AssertionError:
            error_message = []
            try:
                errors = resp.json()
            except json.decoder.JSONDecodeError:
                errors = None
            error_message.append("Failed request for JWT Token.")
            error_message.append("  Response Status Code: {}".format(resp.status_code))
            if not errors == None:
                error_message.append("  Error(s):")
                for k in errors:
                    error_message.append("    {}: {}".format(k,errors[k]))
            raise RuntimeError('\n'.join(error_message))

        data = resp.json()
        token = data.get('access_token',None)
        if debug_level > 1:
            print( "http_status_code: {}".format(resp.status_code) )
            print( "access_token:\n" + token + "\n" )

        return token

    def _get_auth_token(self):
        """Get auth token for MTC"""
        AUTH_URL = self.baseURL + "auth"
        claims = {
        "scope" : "api",
        "grant_type" : "client_credentials"
        }
        payload = claims

        headers = {"Content-Type": "application/json; charset=utf-8"}
        resp = requests.post(AUTH_URL, data=payload, auth=(self.app_id,self.app_secret))

        # Can't do anything without a successful authentication
        try:
            assert resp.status_code == 200
        except AssertionError:
            error_message = []
            try:
                errors = resp.json()
            except json.decoder.JSONDecodeError:
                errors = None
            error_message.append("  Failed request for MTC Auth Token")
            error_message.append("  Response Status Code: {}".format(resp.status_code))
            if not errors == None:
                error_message.append("  Error(s):")
                for k in errors:
                    error_message.append("    {}: {}".format(k,errors[k]))
            raise RuntimeError('\n'.join(error_message))

        data = resp.json()
        token = data.get('access_token',None)
        if debug_level > 1:
            print( "http_status_code: {}".format(resp.status_code) )
            print( "access_token:\n" + token + "\n" )

        return token

    def _make_request(self, method, url, data=None):
        """Request Handler which also checks for token expiration"""
        self.req_cnt += 1

        if datetime.utcnow() > self.access_token_expiration or self.req_cnt >= 9500:
            self.req_cnt = 0
            # Refresh the token if needed
            self.create_conn()
        if method == "get":
            resp = self.s.get(url)
            # loop if rate limited
            # TODO: Improve method when headers are uniformally supported
            while resp.status_code == 429:
                time.sleep(1)
                resp = self.s.get(url)
            return ApiResponse(resp)
        elif method == "post":
            if data:
                return ApiResponse(self.s.post(url, json=data))
            return ApiResponse(self.s.post(url))
        elif method == "delete":
            if data:
                return ApiResponse(self.s.delete(url, json=data))
            return ApiResponse(self.s.delete(url))
        elif method == "put":
            if data:
                return ApiResponse(self.s.put(url, json=data))
            return ApiResponse(self.s.put(url))

        raise ValueError("Invalid Method: {}".format(method))

    def _validate_parameters(self, param, valid_params):

        if param not in valid_params:
            raise ValueError("{} not valid. Valid values are: {}".format(param, valid_params))
        return True

    def _is_valid_detection_status(self, status):

        if status and status not in self.valid_detection_statuses:
            raise ValueError("Status not valid. Valid values: {}".format(self.valid_detection_statuses))
        return True

    def _is_valid_artifact_type(self, artifact_type):

        if artifact_type and artifact_type not in self.valid_artifact_types:
            raise ValueError("Artifact Type not valid. Valid values: {}".format(self.valid_artifact_types))
        return True

    def _convert_id(self,pid):
        # Convert ID to Uppercase & no '-'s
        return pid.replace('-','').upper()

    def _add_url_params(self, url, params):
        """ Add GET params to provided URL being aware of existing.

        :param url: string of target URL
        :param params: dict containing requested params to be added
        :return: string with updated URL

        >> url = 'http://stackoverflow.com/test?answers=true'
        >> new_params = {'answers': False, 'data': ['some','values']}
        >> add_url_params(url, new_params)
        'http://stackoverflow.com/test?data=some&data=values&answers=false'
        """
        # Unquoting URL first so we don't loose existing args
        url = unquote(url)
        # Extracting url info
        parsed_url = urlparse(url)
        # Extracting URL arguments from parsed URL
        get_args = parsed_url.query
        # Converting URL arguments to dict
        parsed_get_args = dict(parse_qsl(get_args))
        # Merging URL arguments dict with new params
        parsed_get_args.update(params)

        parsed_get_args = {k: v for k, v in parsed_get_args.items() if v is not None}
        # Bool and Dict values should be converted to json-friendly values
        # you may throw this part away if you don't like it :)
        parsed_get_args.update(
            {k: json.dumps(v) for k, v in parsed_get_args.items()
             if isinstance(v, (bool, dict))}
        )

        # Converting URL argument to proper query string
        encoded_get_args = urlencode(parsed_get_args, doseq=True)
        # Creating new parsed result object based on provided with new
        # URL arguments. Same thing happens inside of urlparse.
        new_url = ParseResult(
            parsed_url.scheme, parsed_url.netloc, parsed_url.path,
            parsed_url.params, encoded_get_args, parsed_url.fragment
        ).geturl()

        return new_url

    # TODO: Remove this method
    def create_item(self, ptype, item):
        '''Type options: zones, rulesets, policies'''
        baseURL = self.baseURL + "{}/v2".format(ptype)

        if debug_level > 1:
            if debug_level > 2:
                pprint(item)
            print( "Create Item URL: " + baseURL )

        return self._make_request("post",baseURL, data=item)

    # Method to get a page of items and return the response object
    def _get_list_page(self, page_type, page=1, page_size=200, detail="",params={}):
        q_params = {"page": page, "page_size": page_size}

        if params:
            q_params.update(params)

        baseURL = self.baseURL + "{}/v2{}".format(page_type, detail)
        baseURL = self._add_url_params(baseURL, q_params)

        return self._make_request("get",baseURL)

    def _generate_urls(self, page_type, page=1, page_size=200, detail="",params={}, total_pages=0):
            start_page = page
            q_params = {"page": start_page, "page_size": page_size}

            if params:
                q_params.update(params)

            if self.mtc:
                baseURL = self.baseURL + "{}/{}".format(page_type,detail)
            else:
                baseURL = self.baseURL + "{}/v2{}".format(page_type, detail)
                baseURL = self._add_url_params(baseURL, q_params)

            response = self._make_request("get",baseURL)
            try:
                assert response.status_code == 200
            except AssertionError:
                error_message = []
                error_message.append("Failed initial request for {}.".format(page_type))
                error_message.append("  get URL:\n    {}".format(baseURL))
                error_message.append("  Response Status Code: {}".format(response.status_code))
                if response.errors:
                    error_message.append("Error(s)")
                    for k in response.errors:
                        error_message.append("  {}: {}".format(k,response.errors.get(k)))
                raise RuntimeError('\n'.join(error_message))
            data = response.data

            page_size = data['page_size']
            if total_pages == 0 or total_pages > data['total_pages']:
                total_pages = data['total_pages']

            all_urls = [baseURL,]
            for page in range(start_page+1, total_pages+1):
                updated_param = {"page":page}
                baseURL = self._add_url_params(baseURL, updated_param)
                all_urls.append(baseURL)
            # there seems to be a bug which leads to increased 50x errors the higher the page count is (caching?)
            # we want to shuffle the urls so they're not sequentially downloaded anymore and hit the 50x early
            # this way, we can retry again and again, until scalar returns our content
            shuffle(all_urls)
            return all_urls

    def _bulk_get(self, urls, disable_progress=True, paginated=True):

        tqdmargs = {'total': len(urls),
                    'unit': 'Page',
                    'leave': False,
                    'desc': 'Download Progress',
                    'disable': disable_progress}

        collector = []
        with cf.ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            res = {executor.submit(self._make_request, "get", url): url for url in urls}
            for future in tqdm(cf.as_completed(res), **tqdmargs):
                url = res[future]
                try:
                    response = future.result()

                except Exception as exc:
                    print('[-] {} generated an exception: {}'.format(url,exc))
                    continue
                else:
                    try:
                        if not response.is_success:
                            raise json.decoder.JSONDecodeError
                        data = response.data
                        if paginated:
                            collector.extend(data["page_items"])
                        else:
                            collector.append(data)
                    except json.decoder.JSONDecodeError:
                        print("Likely got a Server Error here, trying to quit. Please try again later.")
                        executor.shutdown(wait=False)
                        raise json.decoder.JSONDecodeError
                    except KeyError:
                        print("Error: no data returned.")
                        print("if you see this message, 250 retries per url have been exceeded")
                        print("get a new token and retry later")
                        print("this is the url {} and returned data: {}".format(url, data))

        response.data = collector # This is a hacky way of returning an APIResponse for all of the data

        return response


    # Method to retrieve list of items
    def get_list_items(self, type_name, detail="", limit=200, params={}, disable_progress=True, total_pages=0,
                       start_page=1):

        urls = self._generate_urls(type_name, detail=detail, page_size=limit, params=params, total_pages=total_pages,
                                   page=start_page)

        return self._bulk_get(urls, disable_progress)

    # Method to retrieve an Item
    # This may not be anything as a result of edit error..
    # TODO: Make this return a response instead of a JSON object
    def get_item(self, ptype, item):
        #Type options: rulesets, policies

        if self.mtc:
            baseURL = self.baseURL + "{}/{}".format(ptype, item)
        else:
            baseURL = self.baseURL + "{}/v2/{}".format(ptype, item)

        response = self._make_request("get",baseURL)
        return response

class ApiResponse:
    def __init__(self, response):
        self.status_code = response.status_code
        self.is_success = response.status_code < 300
        self.headers = response.headers
        self.data = None
        self.errors = None

        if self.is_success:
            # 02/29/2021
            # Replacing the commented variables and 'if' in favor
            # of the try/except and re.sub lines to accept
            # non-json values/messages when a successful response
            # is sent.
            # This would omit a 'None' data response.
            """
            try:
                headers = response.headers
                content = headers.get('content-type')
                if content and "json" in content:
                    self.data = response.json()
                else:
                    self.data = response.text
            except json.decoder.JSONDecodeError:
                self.data = None
            """
            try:
                self.data = response.json()
                ####print("Good Data: {}".format(self.data))
            except json.decoder.JSONDecodeError:
                # Removing the wrapper characters of a string response
                self.data = re.sub('{|"|}', "",response.text)

        else:
            try:
                self.errors = response.json()
            except json.decoder.JSONDecodeError:
                self.errors = None

    def to_json(self):
        return {'is_success': self.is_success, 'data': self.data, 'errors': self.errors}

# ---------------------------
# END OF HELPER FUNCTIONS

# Utility Variables
debug_level = 0

if debug_level >= 1:
    print( "Debug level is set at: {}".format(debug_level))
if debug_level >= 5:
    exit("Debug Level too high!")
