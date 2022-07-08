import pytest
import json 

@pytest.mark.case1
def test_vpool(setup):
    cfg, api = setup
    basic_vs_cfg = cfg["BasicVS"]

    resp = api.post('pool', data=json.dumps(basic_vs_cfg["pool_obj"]),
                    api_version=cfg["LoginInfo"]["api_version"])
    assert resp.status_code in (200, 201)
