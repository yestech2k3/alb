import time, logging

from avi.migrationtools.avi_migration_utils import update_count
from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil
import avi.migrationtools.nsxt_converter.converter_constants as conv_const

LOG = logging.getLogger(__name__)

conv_utils = NsxtConvUtil()

class ProfileConfigConv(object):
    def __init__(self, nsxt_profile_attributes):
        """

        """
        self.ap_http_supported_attributes = nsxt_profile_attributes['Application_Http_Profile_supported_attr']
        self.common_na_attr = nsxt_profile_attributes['Common_Na_List']
        self.np_supported_attributes=nsxt_profile_attributes['Network_Profile_supported_attr']

    def convert(self, alb_config, nsx_lb_config, prefix):
        alb_config['ApplicationProfile'] = list()
        alb_config['NetworkProfile'] = list()
        skipped_ap = []
        skipped_np = []
        attr_ap = []
        attr_np = []
        progressbar_count=0
        total_size = len(nsx_lb_config['LbAppProfiles'])
        print("\nConverting Profiles ...")
        LOG.info('Converting Profiles...')
        for lb_pr in nsx_lb_config['LbAppProfiles']:
            try:
                progressbar_count += 1
                name=lb_pr.get('display_name')
                if prefix:
                    name=prefix+'-'+name
                alb_pr = dict(
                    name=name,
                )

                na_list = [val for val in lb_pr.keys()
                           if val in self.common_na_attr]


                if lb_pr['resource_type'] == 'LBHttpProfile':
                    self.convert_http(alb_pr,lb_pr)
                if lb_pr['resource_type'] == 'LBFastUdpProfile':
                    self.convert_udp(alb_pr,lb_pr)
                if lb_pr['resource_type'] == 'LBFastTcpProfile':
                    self.convert_tcp(alb_pr,lb_pr)

                indirect = []
                u_ignore = []
                ignore_for_defaults = {}


                if lb_pr['resource_type'] == 'LBHttpProfile':
                    skipped = [val for val in lb_pr.keys()
                               if val not in self.ap_http_supported_attributes]
                    if lb_pr.get("description"):
                        alb_pr["description"] = lb_pr['description']

                    alb_config['ApplicationProfile'].append(alb_pr)
                    skipped_ap.append(skipped)

                    val=dict(
                        name=alb_pr['name'],
                        resource_type=lb_pr['resource_type'],
                    alb_pr=alb_pr)
                    attr_ap.append(val)

                else:
                    skipped=[val for val in lb_pr.keys()
                             if val not in self.np_supported_attributes]

                    alb_config['NetworkProfile'].append(alb_pr)
                    skipped_np.append(skipped)
                    val = dict(
                        name=alb_pr['name'],
                        resource_type=lb_pr['resource_type'],
                        alb_pr=alb_pr)
                    attr_np.append(val)

                msg = "Profile conversion started..."
                conv_utils.print_progress_bar(progressbar_count, total_size, msg,
                                          prefix='Progress', suffix='')
                # time.sleep(1)
            except:
                update_count('error')
                LOG.error("Failed to convert ApplicationProfile: %s" % lb_pr['display_name'],
                          exc_info=True)
                conv_utils.add_status_row('applicationprofile', None, lb_pr['display_name'],
                                          conv_const.STATUS_ERROR)

        if len(skipped_ap):
            for index, skipped in enumerate(skipped_ap):
                conv_status = conv_utils.get_conv_status(
                skipped, indirect, ignore_for_defaults, nsx_lb_config['LbAppProfiles'],
                u_ignore, na_list)
                conv_utils.add_conv_status('applicationprofile',attr_ap[index]['resource_type'] , attr_ap[index]['name'], conv_status,
                [{'application_http_profile': attr_ap[index]['alb_pr']}])

        if len(skipped_np):
            for index, skipped in enumerate(skipped_np) :
                conv_status = conv_utils.get_conv_status(
                skipped, indirect, ignore_for_defaults, nsx_lb_config['LbAppProfiles'],
                u_ignore, na_list)
                conv_utils.add_conv_status('applicationprofile', attr_np[index]['resource_type'],attr_np[index]['name'], conv_status,
                                               [{'network_profile': attr_np[index]['alb_pr']}])



    def convert_http(self, alb_pr, lb_pr):
        tenant, name = conv_utils.get_tenant_ref("admin")
        alb_pr['tenant_ref'] = conv_utils.get_object_ref(tenant, 'tenant')
        alb_pr['type'] = 'APPLICATION_PROFILE_TYPE_HTTP'
        alb_pr['http-profile']=dict(
            xff_enabled=lb_pr.get('xForwardedFor',False),
            http_to_https=lb_pr.get('httpRedirectToHttps',False),
            keepalive_timeout=lb_pr.get('idle_timeout'),
            client_max_header_size=lb_pr.get('request_header_size'),
            keepalive_header=lb_pr.get('server_keep_alive'),
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

