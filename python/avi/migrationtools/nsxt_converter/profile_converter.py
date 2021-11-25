from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil

conv_utils = NsxtConvUtil()

class ProfileConfigConv(object):
    def __init__(self, nsxt_profile_attributes):
        """

        """

    def convert(self, alb_config, nsx_lb_config, prefix):
        alb_config['ApplicationProfile'] = list()
        alb_config['NetworkProfile'] = list()
        for lb_pr in nsx_lb_config['LbAppProfiles']:
            name=lb_pr.get('display_name')
            if prefix:
                name=prefix+'-'+name
            alb_pr = dict(
                name=name,
            )
            if lb_pr['resource_type'] == 'LBHttpProfile':
                self.convert_http(alb_pr,lb_pr)
            if lb_pr['resource_type'] == 'LBFastUdpProfile':
                self.convert_udp(alb_pr,lb_pr)
            if lb_pr['resource_type'] == 'LBFastTcpProfile':
                self.convert_tcp(alb_pr,lb_pr)

            if lb_pr['resource_type'] == 'LBHttpProfile':
                alb_config['ApplicationProfile'].append(alb_pr)
            else:
                alb_config['NetworkProfile'].append(alb_pr)


    def convert_http(self,alb_pr,lb_pr):
        tenant, name = conv_utils.get_tenant_ref("admin")
        alb_pr['tenant_ref'] = conv_utils.get_object_ref(tenant, 'tenant')
        alb_pr['type'] = 'APPLICATION_PROFILE_TYPE_HTTP'
        alb_pr['http-profile']=dict(
            xff_enabled=lb_pr.get('xForwardedFor',False),
            http_to_https=lb_pr.get('httpRedirectToHttps',False),
            keepalive_timeout=lb_pr.get('idle_timeout'),
            client_max_header_size=lb_pr.get('request_header_size'),
            client_max_body_size=lb_pr.get('requestBodySize')
        )


    def convert_udp(self,alb_pr,lb_pr):
        alb_pr['profile'] = dict(
            type='APPLICATION_PROFILE_TYPE_UDP',
            udp_fast_path_profile=self.fast_profile_path(lb_pr)
        )


    def convert_tcp(self,alb_pr,lb_pr):
        alb_pr['profile'] = dict(
            type='APPLICATION_PROFILE_TYPE_UDP',
            udp_fast_path_profile=self.fast_profile_path(lb_pr)
        )


    def fast_profile_path(self,lb_pr):
        path=dict(
            session_idle_timeout=lb_pr.get('idle_timeout')
        )
        return path

