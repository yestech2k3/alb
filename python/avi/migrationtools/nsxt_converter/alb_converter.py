import argparse
import json
import os
from pprint import PrettyPrinter

SUPPORTED_ALB_OBJECTS = [
"AlertScriptConfig",
"AnalyticsProfile",
"ApplicationPersistenceProfile",
"ApplicationProfile",
"Authprofiles",
"AutoScaleLaunchConfig",
"DnsPolicy",
"ErrorPageBody",
"ErrorPageProfile",
"HardwareSecurityModuleGroup",
"HealthMonitor",
"HTTPPolicySet",
"IpAddrGroup",
"L4PolicySet",
"NetworkProfile",
"NetworkSecurityPolicy",
"ObjectAccessPolicy",
"PingAccessAgent",
"PKIProfile",
"Pool",
"PoolGroup",
"PoolGroupDeploymentPolicy",
"PriorityLabels",
"ProtocolParser",
"SecurityPolicy",
"ServerAutoScalePolicy",
"CertificateManagementProfile",
"SSLKeyAndCertificate",
"SSLProfile",
"SSOPolicy",
"StringGroup",
"TrafficCloneProfile",
"VirtualService",
"VSDataScriptSet",
"VsVip",
"WafCRS",
"WafPolicy",
"WafPolicyPSMGroup",
"WafProfile",
"Webhook"
]

albObjectType = {
    "alertscriptconfig" : "alb-alert-script-configs",
    "analyticsprofile" : "alb-analytics-profiles",
    "applicationpersistenceprofile" : "alb-application-persistence-profiles",
    "applicationprofile" : "alb-application-profiles",
    "authprofile" : "alb-auth-profiles",
    "autoscalelaunchconfig" : "alb-auto-scale-launch-configs",
    "certificatemanagementprofile" : "alb-certificate-management-profiles",
    "dnspolicy" : "alb-dns-policies",
    "errorpagebody" : "alb-error-page-bodies",
    "errorpageprofile" : "alb-error-page-profiles",
    "httppolicyset" : "alb-http-policy-sets",
    "hardwaresecuritymodulegroup" : "alb-hardware-security-module-groups",
    "healthmonitor" : "alb-health-monitors",
    "ipaddrgroup" : "alb-ip-addr-groups",
    "l4policyset" : "alb-l4-policy-sets",
    "networkprofile" : "alb-network-profiles",
    "networksecuritypolicy" : "alb-network-security-policies",
    "pkiprofile" : "alb-pki-profiles",
    "pingaccessagent" : "alb-ping-access-agents",
    "pool" : "alb-pools",
    "poolgroup" : "alb-pool-groups",
    "poolgroupdeploymentpolicy" : "alb-pool-group-deployment-policies",
    "prioritylabels" : "alb-priority-labels",
    "protocolparser" : "alb-protocol-parsers",
    "sslkeyandcertificate" : "alb-ssl-key-and-certificates",
    "sslprofile" : "alb-ssl-profiles",
    "ssopolicy" : "alb-sso-policies",
    "securitypolicy" : "alb-security-policies",
    "serverautoscalepolicy" : "alb-server-auto-scale-policies",
    "stringgroup" : "alb-string-groups",
    "trafficcloneprofile" : "alb-traffic-clone-profiles",
    "vsdatascriptset" : "alb-vs-data-script-sets",
    "virtualservice" : "alb-virtual-services",
    "vsvip" : "alb-vs-vips",
    "wafcrs" : "alb-waf-crs",
    "wafpolicy" : "alb-waf-policies",
    "wafpolicypsmgroup" : "alb-waf-policy-psm-groups",
    "wafprofile" : "alb-waf-profiles",
    "objectaccesspolicy" : "alb-object-access-policies",
    "webhook" : "alb-webhooks"
}

# SUPPORTED_ALB_OBJECTS = ['VirtualService']

NOT_APPLICABLE = ['url', 'uuid', 'tenant_ref']
REPLACE_KEYS = ['name', 'cloud_ref', 'vrf_ref', 'vrf_context_ref', 'tier1_lr']

class ALBConverter:
    def __init__(self, args):
        '''

        '''
        self.avi_config_file = args.avi_config_file
        self.output_file_path = args.output_file_path if args.output_file_path \
            else 'output-alb'

    def convert(self):
        if not os.path.exists(self.output_file_path):
            os.mkdir(self.output_file_path)
        output_dir = os.path.normpath(self.output_file_path)
        input_path = output_dir + os.path.sep + os.path.sep + "input-alb"
        if not os.path.exists(input_path):
            os.makedirs(input_path)
        input_config = input_path + os.path.sep + "config.json"
        with open(self.avi_config_file, "r") as read_file:
            avi_config = json.load(read_file)

        with open(input_config, "w", encoding='utf-8') as text_file:
            json.dump(avi_config, text_file, indent=4)

        alb_config = self.convert_to_alb(avi_config)
        pp = PrettyPrinter()
        pp.pprint(alb_config)

        output_path = output_dir + os.path.sep + os.path.sep + "output-alb"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_config = output_path + os.path.sep + "alb_config.json"
        with open(output_config, "w", encoding='utf-8') as text_file:
            json.dump(alb_config, text_file, indent=4)

    def convert_to_alb(self, avi_config):
        alb_config = dict()
        for key in avi_config.keys():
            if key in SUPPORTED_ALB_OBJECTS:
                config = []
                supported_obj = avi_config[key]
                for obj in supported_obj:
                    data = self.recursive_items(obj, {})
                    config.append(data)
                alb_config[key] = config
        return alb_config

    def recursive_items(self, obj, data):
        for k, v in obj.items():
            if k not in NOT_APPLICABLE:
                if type(v) is dict:
                    data[k] = self.recursive_items(v, {})
                elif not k.endswith("_refs") and type(v) is list:
                    tmp = []
                    for iter_over_obj in v:
                        if type(iter_over_obj) is dict:
                            tmp.append(self.recursive_items(iter_over_obj, {}))
                        else:
                            tmp.append(iter_over_obj)
                    data[k] = tmp
                elif k in REPLACE_KEYS:
                    if k == REPLACE_KEYS[0]:
                        data['display_name'] = v
                        data['id'] = v
                    if k == REPLACE_KEYS[1]:
                        data['cloud_name'] = v.split("name=")[1]
                    if k == REPLACE_KEYS[2]:
                        data['vrf_name'] = v.split("name=")[1].split("&")[0]
                    if k == REPLACE_KEYS[3]:
                        data['vrf_context_name'] = v.split("name=")[1].split("&")[0]
                    if k == REPLACE_KEYS[4]:
                        data["tier1_path"] = v
                elif k.endswith("_ref"):
                    if v.split('/')[2] not in albObjectType.keys():
                        continue
                    object_type = albObjectType[v.split('/')[2]]
                    data[k.replace("_ref", "_path")] = "/infra/" + object_type + "/" + v.split("name=")[1]
                elif k.endswith("_refs"):
                    list_of_paths = [ "/infra/" + albObjectType[data.split('/')[2]] + "/" + data.split("name=")[1] for data in v ]
                    data[k.replace("_refs", "_paths")] = list_of_paths
                else:
                    data[k] = v
        return data


if __name__ == "__main__":
    HELP_STR = '''
       Converts AVI Config to ALB config.
       Example to convert AVI config file to ALB config json:
            alb_converter.py -f tmp_exported_config.json
       '''

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=(HELP_STR))

    # Added args for baseline profile json file
    parser.add_argument('-f', '--avi_config_file',
                        help='absolute path for avi config file')
    parser.add_argument('-o', '--output_file_path',
                        help='Folder path for output files to be created in',
                        )

    args = parser.parse_args()

    alb_converter = ALBConverter(args)
    alb_converter.convert()