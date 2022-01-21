
from avi.migrationtools.nsxt_converter import nsxt_client as nsx_client_util
import pprint
pp = pprint.PrettyPrinter(indent=4)
class NSXUtil():

    nsx_api_client = None

    def __init__(self, nsx_un, nsx_pw, nsx_ip, nsx_port):
        self.nsx_api_client = nsx_client_util.create_nsx_policy_api_client(
            nsx_un, nsx_pw, nsx_ip, nsx_port, auth_type=nsx_client_util.BASIC_AUTH)

    def get_nsx_config(self):
        nsx_lb_config = dict()
        nsx_lb_config["LBServices"] = self.nsx_api_client.infra.LbServices.list().to_dict().get("results", [])
        nsx_lb_config["LbMonitorProfiles"] = self.nsx_api_client.infra.LbMonitorProfiles.list().to_dict().get("results", [])
        nsx_lb_config["LbPools"] = self.nsx_api_client.infra.LbPools.list().to_dict().get("results", [])
        nsx_lb_config["LbAppProfiles"] = self.nsx_api_client.infra.LbAppProfiles.list().to_dict().get("results", [])
        nsx_lb_config["LbClientSslProfiles"] = self.nsx_api_client.infra.LbClientSslProfiles.list().to_dict()["results"]
        nsx_lb_config["LbServerSslProfiles"] = self.nsx_api_client.infra.LbServerSslProfiles.list().to_dict()["results"]
        nsx_lb_config["LbPersistenceProfiles"] = self.nsx_api_client.infra.LbPersistenceProfiles.list().to_dict()["results"]
        nsx_lb_config['LbVirtualServers'] = self.nsx_api_client.infra.LbVirtualServers.list().to_dict().get('results',[])
        return nsx_lb_config

    def upload_alb_config(self, alb_config):
        if alb_config.get("alb-health-monitors"):
            self.upload_monitor_alb_config(alb_config.get("alb-health-monitors"))

    def upload_monitor_alb_config(self, alb_hm_config):

        for hm in alb_hm_config:
            is_create_hm = False
            try:
                hm_obj = self.nsx_api_client.infra.AlbHealthMonitors.get(hm["id"])
                print(hm_obj)
            except Exception as e:
                print(e)
                is_create_hm = True
            if is_create_hm:
                try:
                    alb_hm_obj = self.nsx_api_client.infra.AlbHealthMonitors.update(hm["id"], hm)
                    print(alb_hm_obj)
                except Exception as e:
                    print(e)


import json
if __name__ == "__main__":
    path = "/Users/sagar/git-source/sdk2/TALB/talb/alb-sdk/python/avi/migrationtools/nsxt_converter/output/10.191.226.85/output/alb_config.json"
    f = open(path)
    alb_config = json.load(f)
    util = NSXUtil("admin", "Admin!23Admin", "10.191.226.85", "443")
    util.upload_alb_config(alb_config)


