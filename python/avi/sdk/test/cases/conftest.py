import pytest
import json


import sys
sys.path.append("/home/ubuntu/alb/alb/python")

from avi.sdk.avi_api import (ApiSession, ObjectNotFound, APIError, ApiResponse,
                             avi_timedelta, sessionDict,
                             AviMultipartUploadError)
from avi.sdk.utils.api_utils import ApiUtils
from avi.sdk.samples.common import get_sample_ssl_params
from avi.sdk.samples.clone_vs import AviClone

def pytest_addoption(parser):
    parser.addoption("--config", action="store", help="config file")

@pytest.fixture(scope='module') 
def setup(request): 

    print("setup: read the cfg")
    config_file = request.config.getoption("--config")
    with open(config_file) as fp_config:
        cfg = json.load(fp_config)
    login_info = cfg["LoginInfo"]

    print("setup: create the apisession")
    api = ApiSession(
        login_info["controller_ip"], login_info.get("username", "admin"),
        login_info.get("password", "fr3sca$%^"), api_version=login_info.get(
            "api_version", "17.1"), data_log=login_info['data_log'])    

    yield (cfg, api)

    print("teardown: teardown")
