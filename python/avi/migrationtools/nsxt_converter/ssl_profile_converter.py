from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil

conv_utils = NsxtConvUtil()


class SslProfileConfigConv(object):
    def __init__(self, nsxt_profile_attributes):
        """

        """

    def convert(self, alb_config, nsx_lb_config, prefix):
        alb_config["SSLProfile"] = []
        for lb_ssl in nsx_lb_config["LbClientSslProfiles"]:
            name = lb_ssl.get('display_name')
            if prefix:
                name = prefix + '-' + name
            alb_ssl = dict(
                name=name,
            )
            if lb_ssl.get("session_cache_enabled"):
                alb_ssl['enable_ssl_session_reuse'] = lb_ssl['session_cache_enabled']
            if lb_ssl.get("session_cache_timeout"):
                alb_ssl['ssl_session_timeout'] = lb_ssl['session_cache_timeout']

            if lb_ssl.get("ciphers"):
                alb_ssl['accepted_ciphers'] = ":".join(lb_ssl['ciphers'])

            if lb_ssl.get("protocols"):
                self.convert_protocols(lb_ssl['protocols'], alb_ssl)

            alb_config['SSLProfile'].append(alb_ssl)

    def convert_protocols(self, protocols, alb_ssl):
        alb_ssl['accepted_versions'] = []

        for acc_ver in protocols:
            acc_version = dict(
                type=acc_ver
            )
            alb_ssl['accepted_versions'].append(acc_version)
