import pytest
import json 

@pytest.mark.case1
def test_vs(setup):
    cfg, api = setup
    basic_vs_cfg = cfg["BasicVS"]

    #create pool
    resp = api.post('pool', data=json.dumps(basic_vs_cfg["pool_obj"]),
                    api_version=cfg["LoginInfo"]["api_version"])
    assert resp.status_code in (200, 201)
    basic_vs_cfg["vs_obj"]["pool_ref"] = api.get_obj_ref(resp.json())

    #create vip
    resp = api.post('vsvip', data=json.dumps(basic_vs_cfg["vsvip_obj"]),
                    api_version=cfg["LoginInfo"]["api_version"])
    assert resp.status_code in (200, 201)
    basic_vs_cfg["vs_obj"]["vsvip_ref"] = api.get_obj_ref(resp.json())

    #create vs
    resp = api.post('virtualservice', data=json.dumps(basic_vs_cfg["vs_obj"]),
                    api_version=cfg["LoginInfo"]["api_version"])
    assert resp.status_code in (200, 201)
