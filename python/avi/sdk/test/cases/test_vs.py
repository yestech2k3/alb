import pytest
import json
import pdb
import os
from avi.sdk.samples.common import get_sample_ssl_params
from avi.sdk.utils.api_utils import ApiUtils
from avi.sdk.samples.virtualservice_examples_api import VirtualService
from avi.sdk.avi_api import (ApiSession, ObjectNotFound, APIError, ApiResponse,
                             avi_timedelta, sessionDict,
                             AviMultipartUploadError)

@pytest.mark.usefixtures("setup","csetup")
class TestVS:

    @pytest.mark.case1
    def test_basic_vs(self,setup):
        cfg, api = setup
        basic_vs_cfg = cfg["BasicVS"]

        #create pool
        resp = api.post('pool', data=json.dumps(basic_vs_cfg["pool_obj"]),
                        api_version=cfg["LoginInfo"]["api_version"])
        assert resp.status_code in (200, 201),resp.json()
        basic_vs_cfg["vs_obj"]["pool_ref"] = api.get_obj_ref(resp.json())
        
        #create vip
        resp = api.post('vsvip', data=json.dumps(basic_vs_cfg["vsvip_obj"]),
                        api_version=cfg["LoginInfo"]["api_version"])
        assert resp.status_code in (200, 201),resp.json()
        basic_vs_cfg["vs_obj"]["vsvip_ref"] = api.get_obj_ref(resp.json())

        #create vs
        resp = api.post('virtualservice', data=json.dumps(basic_vs_cfg["vs_obj"]),
                        api_version=cfg["LoginInfo"]["api_version"])
        assert resp.status_code in (200, 201),resp.json()
    
    @pytest.mark.case2
    def test_ssl_vs(self,setup):
        cfg, api = setup
        basic_vs_cfg = cfg["SSL-VS"]

        #create pool
        resp = api.post('pool', data=json.dumps(basic_vs_cfg["pool_obj"]),
                        api_version=cfg["LoginInfo"]["api_version"])
        assert resp.status_code in (200, 201),resp.json()
        basic_vs_cfg["vs_obj"]["pool_ref"] = api.get_obj_ref(resp.json())

        #create vip
        resp = api.post('vsvip', data=json.dumps(basic_vs_cfg["vsvip_obj"]),
                        api_version=cfg["LoginInfo"]["api_version"])
        assert resp.status_code in (200, 201),resp.json()
        basic_vs_cfg["vs_obj"]["vsvip_ref"] = api.get_obj_ref(resp.json())

        #create cert
        path = os.getcwd()
        cert, key = get_sample_ssl_params(path+"/")
        api_utils = ApiUtils(api)
        resp = api_utils.import_ssl_certificate("cert1", key, cert)
        if resp.status_code not in range(201, 299):
            print('Error in uploading certs : %s' % resp.text)
            exit(0)
        ssl_kc_ref = api.get_obj_ref(resp)

        #create vs based on ssl
        basic_vs_cfg = cfg["SSL-VS"]
        basic_vs_cfg["vs_obj"]["ssl_key_and_certificate_refs"] = [ssl_kc_ref]
        resp = api.post('virtualservice', data=json.dumps(basic_vs_cfg["vs_obj"]),
                        api_version=cfg["LoginInfo"]["api_version"])
        assert resp.status_code in (200, 201),resp.json()

    #case3
        #Create tenant-test
        #Verify new pool not present in tenant admin (api)
        #Verify new pool present in tenant-test (tapi)
        #Verify pool access by using admin api but by refering tenant_uuid
        #Verify pool access by using admin api but by refering tenant name
        #Verify response after pool delete (tapi)
        #Verify pool access returns None, by using admin api but by refering tenant name
        #Verify tenant delete (test-tenant) using tapi

    @pytest.mark.case3
    def test_basic_vs_multi_tenant(self,setup):
        cfg, api = setup

        #Create tenant-test
        # resp = api.post('tenant', data=json.dumps({"name": "tenant-test"}),
        #                 api_version=cfg["LoginInfo"]["api_version"])
        # assert resp.status_code in (200, 201),resp.json()

        login_info = cfg["LoginInfo"]
        tapi = ApiSession(
            login_info["controller_ip"], login_info.get("username", "admin"),
            login_info.get("password", "fr3sca$%^"), tenant="tenant-test", api_version=login_info.get(
                "api_version", "17.1"), data_log=login_info['data_log'])

        vs1_tapi = VirtualService(tapi)
        assert vs1_tapi.create_basic_vs("vs-tenant","vs-tenant-vip","1.1.1.1","vs-tenant-pool",["2.2.2.2","3.3.3.3"])==True

        # Verify new pool not present in tenant admin (api)
        # Verify new pool present in tenant-test (tapi)
        # Verify pool access by using admin api but by refering tenant_uuid
        # Verify pool access by using admin api but by refering tenant name
        # Verify response after pool delete (tapi)
        # Verify pool access returns None, by using admin api but by refering tenant name
        # Verify tenant delete (test-tenant) using tapi


        # basic_vs_cfg = cfg["BasicVS"]

        # #create pool
        # resp = api.post('pool', data=json.dumps(basic_vs_cfg["pool_obj"]),
        #                 api_version=cfg["LoginInfo"]["api_version"])
        # assert resp.status_code in (200, 201),resp.json()
        # basic_vs_cfg["vs_obj"]["pool_ref"] = api.get_obj_ref(resp.json())
        
        # #create vip
        # resp = api.post('vsvip', data=json.dumps(basic_vs_cfg["vsvip_obj"]),
        #                 api_version=cfg["LoginInfo"]["api_version"])
        # assert resp.status_code in (200, 201),resp.json()
        # basic_vs_cfg["vs_obj"]["vsvip_ref"] = api.get_obj_ref(resp.json())

        # #create vs
        # resp = api.post('virtualservice', data=json.dumps(basic_vs_cfg["vs_obj"]),
        #                 api_version=cfg["LoginInfo"]["api_version"])
        # assert resp.status_code in (200, 201),resp.json()
