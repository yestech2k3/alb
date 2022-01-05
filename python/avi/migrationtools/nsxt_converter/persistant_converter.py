import logging
import os

from avi.migrationtools.avi_migration_utils import update_count
from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil
import avi.migrationtools.nsxt_converter.converter_constants as final
import avi.migrationtools.nsxt_converter.converter_constants as conv_const


LOG = logging.getLogger(__name__)

conv_utils = NsxtConvUtil()
class PersistantProfileConfigConv(object):
    def __init__(self, nsxt_profile_attributes):
        """

        """
        self.supported_attr = nsxt_profile_attributes['PersistenceProfile_Supported_Attributes']
        self.supported_attr_cookie = nsxt_profile_attributes['CookiePersistenceProfile_Supported_Attributes']
        self.supported_attr_source = nsxt_profile_attributes['SourcePersistenceProfile_Supported_Attributes']
        self.common_na_attr = nsxt_profile_attributes['Common_Na_List']
        #TODO
        self.object_merge_check = None
        self.certkey_count = 0


    def convert(self, alb_config, nsx_lb_config, prefix):
        alb_config["ApplicationPersistenceProfile"] = []
        # Added variable to get total object count.
        progressbar_count = 0
        total_size = len(nsx_lb_config['LbPersistenceProfiles'])
        print("\nConverting Persistence Profile ...")
        LOG.info('[ApplicationPersistenceProfile] Converting Profiles...')
        for lb_pp in nsx_lb_config["LbPersistenceProfiles"]:
            try:
                LOG.info('[ApplicationPersistenceProfile] Migration started for  {}'.format(lb_pp['display_name']))
                progressbar_count += 1
                if lb_pp['resource_type'] == 'LBGenericPersistenceProfile':
                    conv_utils.add_status_row('persistence', lb_pp['resource_type'], lb_pp['display_name'],
                                              conv_const.STATUS_SKIPPED)
                    continue

                pp_type, name = self.get_name_type(lb_pp)

                na_list = [val for val in lb_pp.keys()
                           if val in self.common_na_attr]
                if prefix:
                    name = prefix + '-' + name

                alb_pp = dict(
                    name=name
                )
                skipped = [val for val in lb_pp.keys()
                           if val not in self.supported_attr]

                cookie_skipped_list,source_skipped_list = [],[]
                if pp_type == "LBCookiePersistenceProfile":
                    skipped, cookie_skipped_list = self.convert_cookie(lb_pp, alb_pp, skipped, "admin")
                elif pp_type == "LBSourceIpPersistenceProfile":
                    skipped = self.convert_source(lb_pp, alb_pp, skipped, "admin")


                if cookie_skipped_list:
                    skipped.append(cookie_skipped_list)
                if source_skipped_list:
                    skipped.append(source_skipped_list)


                indirect = []
                u_ignore = []
                ignore_for_defaults = {}
                conv_status = conv_utils.get_conv_status(
                    skipped, indirect, ignore_for_defaults, nsx_lb_config['LbMonitorProfiles'],
                    u_ignore, na_list)

                conv_utils.add_conv_status('persistence', pp_type, alb_pp['name'], conv_status,
                                           [{'app_per_profile': alb_pp}])

                alb_config['ApplicationPersistenceProfile'].append(alb_pp)
                msg = "ApplicationPersistenceProfile conversion started..."
                conv_utils.print_progress_bar(progressbar_count, total_size, msg,
                                              prefix='Progress', suffix='')
                # time.sleep(1)
                if len(conv_status['skipped']) > 0:
                    LOG.debug('[ApplicationPersistenceProfile] Skipped Attribute {}:{}'.format(lb_pp['display_name'], conv_status['skipped']))

                LOG.info('[ApplicationPersistenceProfile] Migration completed for HM {}'.format(lb_pp['display_name']))

            except Exception as e:
                update_count('error')
                LOG.error("[ApplicationPersistenceProfile] Failed to convert ApplicationPersistenceProfile: %s" % lb_pp['display_name'],
                          exc_info=True)
                conv_utils.add_status_row('persistence', None, lb_pp['display_name'],
                                              conv_const.STATUS_ERROR)

    def get_name_type(self, lb_pp):
        """

        """
        return lb_pp['resource_type'], lb_pp['display_name']

    def convert_cookie(self, lb_pp, alb_pp, skipped, tenant):
        http_cookie_persistence_profile = {}
        skipped_list = []
        final_skiped_attr = []
        if lb_pp.get("cookie_name"):
            http_cookie_persistence_profile["cookie_name"] = lb_pp.get("cookie_name")

        if lb_pp.get("cookie_time", None):
            http_cookie_persistence_profile["timeout"] = lb_pp.get("cookie_time")['cookie_max_idle']
            for index, i in enumerate(skipped):
                if i == "cookie_time":
                    del skipped[index]
            _skipped = [key for key in lb_pp.get("cookie_time").keys()
                       if key not in self.supported_attr_cookie]
            for keys in _skipped:
                final_skiped_attr.append(keys)


        alb_pp['http_cookie_persistence_profile'] = http_cookie_persistence_profile
        alb_pp['tenant_ref'] = conv_utils.get_object_ref(
            tenant, 'tenant')
        alb_pp['persistence_type'] = "PERSISTENCE_TYPE_HTTP_COOKIE"

        if final_skiped_attr:
            skipped_list.append({lb_pp['display_name']: final_skiped_attr})
        skipped = [key for key in skipped if key not in self.supported_attr_cookie]
        return skipped, skipped_list


    def convert_source(self, lb_pp, alb_pp, skipped, tenant):
        ip_persistence_profile = {}
        if lb_pp.get("timeout"):
            ip_persistence_profile["ip_persistent_timeout"] = lb_pp.get("timeout")

        alb_pp['ip_persistence_profile'] = ip_persistence_profile
        alb_pp['tenant_ref'] = conv_utils.get_object_ref(
            tenant, 'tenant')
        alb_pp['persistence_type'] = "PERSISTENCE_TYPE_CLIENT_IP_ADDRESS"

        skipped = [key for key in skipped if key not in self.supported_attr_source]
        return skipped