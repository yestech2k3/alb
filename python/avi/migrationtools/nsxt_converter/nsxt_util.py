
from avi.migrationtools.nsxt_converter import nsxt_client as nsx_client_util
import pprint
pp = pprint.PrettyPrinter(indent=4)
class NSXUtil():

    nsx_api_client = None

    def __init__(self, nsx_un, nsx_pw, nsx_ip, nsx_port):
        self.nsx_api_client = nsx_client_util.create_nsx_policy_api_client(
            nsx_un, nsx_pw, nsx_ip, nsx_port, auth_type=nsx_client_util.SESSION_AUTH)

    def get_nsx_config(self):
        nsx_lb_config = dict()
        nsx_lb_config["LBServices"] = self.nsx_api_client.infra.LbServices.list().to_dict().get("results", [])
        nsx_lb_config["LbMonitorProfiles"] = self.nsx_api_client.infra.LbMonitorProfiles.list().to_dict().get("results", [])
        nsx_lb_config["LbPools"] = self.nsx_api_client.infra.LbPools.list().to_dict().get("results", [])
        nsx_lb_config["LbAppProfiles"] = self.nsx_api_client.infra.LbAppProfiles.list().to_dict().get("results", [])
        nsx_lb_config["LbClientSslProfiles"] = self.nsx_api_client.infra.LbClientSslProfiles.list().to_dict()["results"]
        nsx_lb_config["LbServerSslProfiles"] = self.nsx_api_client.infra.LbServerSslProfiles.list().to_dict()["results"]
        nsx_lb_config['LbVirtualServers'] = self.nsx_api_client.infra.LbVirtualServers.list().to_dict().get('results',[])
        nsx_lb_config["LbPersistenceProfiles"] = self.nsx_api_client.infra.LbPersistenceProfiles.list().to_dict()["results"]
        return nsx_lb_config

