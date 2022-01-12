import logging

from avi.migrationtools.avi_migration_utils import MigrationUtil
from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil
from avi.migrationtools.avi_migration_utils import update_count
import avi.migrationtools.nsxt_converter.converter_constants as conv_const

LOG = logging.getLogger(__name__)

conv_utils = NsxtConvUtil()
common_avi_util = MigrationUtil()


class VsConfigConv(object):
    def __init__(self, nsxt_profile_attributes, object_merge_check, merge_object_mapping, sys_dict):
        """

        """
        self.supported_attr = nsxt_profile_attributes['VS_supported_attr']
        self.server_ssl_attr = nsxt_profile_attributes['VS_server_ssl_supported_attr']
        self.client_ssl_attr = nsxt_profile_attributes['VS_client_ssl_supported_attr']
        self.common_na_attr = nsxt_profile_attributes['Common_Na_List']
        self.object_merge_check = object_merge_check
        self.merge_object_mapping = merge_object_mapping
        self.sys_dict = sys_dict

    def convert(self, alb_config, nsx_lb_config, cloud_name, prefix, vs_state, controller_version,vrf=None):
        '''
        LBVirtualServer to Avi Config vs converter
        '''

        alb_config['VirtualService'] = list()
        alb_config['VsVip'] = []
        progressbar_count = 0
        total_size = len(nsx_lb_config['LbVirtualServers'])
        print("\nConverting Virtual Services ...")
        LOG.info('[Virtual Service ] Converting Services...')

        for lb_vs in nsx_lb_config['LbVirtualServers']:
            try:
                progressbar_count += 1
                LOG.info('[Virtual Service] Migration started for VS {}'.format(lb_vs['display_name']))
                #vs_name = lb_vs['name']
                name = lb_vs.get('display_name')
                if prefix:
                    name = prefix + '-' + name
                vs_name = name
                alb_vs = dict(
                    name=name,
                    enabled=lb_vs.get('enabled'),
                    cloud_ref=conv_utils.get_object_ref(cloud_name, 'cloud')

                )
                tier1_lr = ''
                for ref in nsx_lb_config['LBServices']:
                    if lb_vs['lb_service_path'] == ref['path']:
                        tier1_lr = ref['connectivity_path']

                if lb_vs.get('ip_address'):
                    vip = dict(
                        name=name + '-vsvip',
                        tier1_lr=tier1_lr,
                        cloud_ref=conv_utils.get_object_ref(cloud_name, 'cloud'),
                        vip=[
                            dict(
                                ip_address=dict(
                                    addr=lb_vs.get('ip_address'),
                                    type='V4'
                                )
                            )
                        ]

                    )
                    alb_config['VsVip'].append(vip)
                    vsvip_ref = '/api/vsvip/?tenant=admin&name=%s&cloud=%s' % (name + '-vsvip', cloud_name)
                    alb_vs['vsvip_ref'] = vsvip_ref
                alb_vs['services'] = [
                    dict(
                        port=lb_vs.get('ports')[0]
                    )]
                skipped = [val for val in lb_vs.keys()
                           if val not in self.supported_attr]
                na_list = [val for val in lb_vs.keys()
                           if val in self.common_na_attr]

                if lb_vs.get('application_profile_path'):
                    profile_path = lb_vs.get('application_profile_path')
                    profile_name = profile_path.split('/')[-1]
                    app_profile_ref = self.get_vs_app_profile_ref(alb_config['ApplicationProfile'],
                                                                  profile_name, self.object_merge_check,
                                                                  self.merge_object_mapping, prefix)
                    if app_profile_ref.__contains__("networkprofile"):
                        alb_vs['network_profile_ref']=app_profile_ref
                    else:
                        alb_vs['application_profile_ref'] = app_profile_ref
                if lb_vs.get('max_concurrent_connections'):
                    alb_vs['performance_limits'] = dict(
                        max_concurrent_connections=lb_vs.get('max_concurrent_connections')
                    )
                if lb_vs.get('client_ssl_profile_binding'):
                    if lb_vs['client_ssl_profile_binding'].get('ssl_profile_path'):
                        ssl_ref = lb_vs['client_ssl_profile_binding']['ssl_profile_path'].split('/')[-1]
                        if prefix:
                            ssl_ref = prefix + '-' + ssl_ref
                        alb_vs['ssl_profile_ref'] = '/api/sslprofile/?tenant=admin&name=' + ssl_ref
                    skipped = [val for val in skipped
                               if val not in self.client_ssl_attr]
                if lb_vs.get('pool_path'):
                    pool_ref = lb_vs.get('pool_path')
                    pool_name = pool_ref.split('/')[-1]
                    if prefix:
                        pool_name = prefix + '-' + pool_name
                    alb_vs['pool_ref'] = '/api/pool/?tenant=admin&name=' + pool_name
                    if lb_vs.get('server_ssl_profile_binding'):
                        self.update_pool_with_ssl(alb_config, lb_vs, pool_name, self.object_merge_check,
                                                  self.merge_object_mapping, prefix)
                        skipped = [val for val in skipped
                                   if val not in self.server_ssl_attr]
                if lb_vs.get('lb_persistence_profile_path'):
                    self.update_pool_with_persistence(alb_config['Pool'], lb_vs,
                                                      pool_name, self.object_merge_check, self.merge_object_mapping,
                                                      prefix)

                for pool in alb_config['Pool']:
                    if pool.get('name') == pool_name:
                        if lb_vs.get('default_pool_member_ports'):
                            pool['default_port'] = lb_vs['default_pool_member_ports']
                        pool['tier1_lr'] = tier1_lr
                indirect = []
                u_ignore = []
                ignore_for_defaults = {}
                conv_status = conv_utils.get_conv_status(
                    skipped, indirect, ignore_for_defaults, nsx_lb_config['LbVirtualServers'],
                    u_ignore, na_list)
                conv_utils.add_conv_status('virtual', lb_vs['resource_type'], alb_vs['name'], conv_status,
                                           alb_vs)
                alb_config['VirtualService'].append(alb_vs)

                msg = "Server conversion started..."
                conv_utils.print_progress_bar(progressbar_count, total_size, msg,
                                              prefix='Progress', suffix='')
                if len(conv_status['skipped']) > 0:
                    LOG.debug('[VirtualService] Skipped Attribute {}:{}'.format(lb_vs['display_name'],
                                                                                conv_status['skipped']))

                LOG.info('[VirtualService] Migration completed for HM {}'.format(lb_vs['display_name']))
            except:
                update_count('error')
                LOG.error("[VirtualServer] Failed to convert Monitor: %s" % lb_vs['display_name'],
                          exc_info=True)
                conv_utils.add_status_row('virtual', None, lb_vs['display_name'],
                                          conv_const.STATUS_ERROR)

    def update_pool_with_ssl(self, alb_config, lb_vs, pool_name, object_merge_check, merge_object_mapping, prefix):
        for pool in alb_config['Pool']:
            if pool.get('name') == pool_name:
                if lb_vs['server_ssl_profile_binding'].get('ssl_profile_path'):
                    ssl_ref = prefix + '-' + lb_vs['server_ssl_profile_binding']['ssl_profile_path'].split('/')[-1]
                    if object_merge_check:
                        ssl_name = merge_object_mapping['ssl_profile'].get(ssl_ref)
                        if ssl_name:
                            ssl_ref = ssl_name
                    pool['ssl_profile_ref'] = '/api/sslprofile/?tenant=admin&name=' + ssl_ref

    def update_pool_with_persistence(self, alb_pool_config, lb_vs, pool_name, object_merge_check, merge_object_mapping,
                                     prefix):
        for pool in alb_pool_config:
            if pool.get('name') == pool_name:
                persistence_ref = prefix + '-' + lb_vs.get('lb_persistence_profile_path').split('/')[-1]
                pool['persistence_profile_ref'] = '/api/persistenceprofile/?tenant=admin&name=' + persistence_ref

    def get_vs_app_profile_ref(self, alb_profile_config, profile_name, object_merge_check,
                               merge_object_mapping, prefix):
        if prefix:
            profile_name = prefix + '-' + profile_name
        if object_merge_check:
            app_profile_merge_name = merge_object_mapping['app_profile'].get(profile_name)
            if app_profile_merge_name:
                profile_name = app_profile_merge_name
            np_prodile_merge_name=merge_object_mapping['network_profile'].get(profile_name)
            if np_prodile_merge_name:
                profile_name=np_prodile_merge_name
                return '/api/networkprofile/?tenant=admin&name=' + profile_name

        return '/api/applicationprofile/?tenant=admin&name=' + profile_name

