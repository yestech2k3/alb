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
import time

def pytest_addoption(parser):
    parser.addoption("--config", action="store", help="config file")

@pytest.fixture(scope='module')
def setup(request):
    print("\nsetup: read the cfg")
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

@pytest.fixture(scope="class")
def csetup(setup):
    cfg,api = setup
    yield
    print("\nTeardown: teardown")

    def cleanup(type,name):
        print("Deleting {} with name {}".format(type,name))
        try:
            api.delete_by_name(type,name)
        except Exception as e:
            print("cleanup failed for {} with msg {}".format(name,str(e)))
        time.sleep(5)

    #cleanup vs
    all_vs_iter = api.get_objects_iter('virtualservice')
    for vs in all_vs_iter:
        cleanup('virtualservice',vs["name"])
    #cleanup vsvip        
    all_vsvip_iter = api.get_objects_iter('vsvip')
    for vsvip in all_vsvip_iter:
        cleanup('vsvip',vsvip["name"])
    #cleanup pool
    all_pools_iter = api.get_objects_iter('pool')
    for pool in all_pools_iter:
        cleanup('pool',pool["name"])
    #cleanup cert
    default_cert = ["System-Default-Cert","System-Default-Cert-EC","System-Default-Portal-Cert",
                    "System-Default-Portal-Cert-EC256","System-Default-Secure-Channel-Cert","System-Default-Root-CA"]
    all_cert_iter = api.get_objects_iter('sslkeyandcertificate')
    for cert in all_cert_iter:
        if cert["name"] not in default_cert:
            cleanup('sslkeyandcertificate',cert["name"])