import logging

from avi.migrationtools.avi_migration_utils import MigrationUtil
from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil
from avi.migrationtools.avi_migration_utils import update_count
import avi.migrationtools.nsxt_converter.converter_constants as conv_const
import avi.migrationtools.nsxt_converter.converter_constants as final

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
        self.VS_na_attr=nsxt_profile_attributes["VS_na_list"]
        self.object_merge_check = object_merge_check
        self.merge_object_mapping = merge_object_mapping
        self.sys_dict = sys_dict
        self.certkey_count = 0

    def convert(self, alb_config, nsx_lb_config, cloud_name, prefix,tenant, vs_state, controller_version,
                vrf=None,segroup=None):
        '''
        LBVirtualServer to Avi Config vs converter
        '''
        converted_alb_ssl_certs = list()
        alb_config['VirtualService'] = list()
        alb_config['VsVip'] = list()
        alb_config['SSLKeyAndCertificate'] = list()

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
                alb_vs = dict(
                    name=name,
                    enabled=lb_vs.get('enabled'),
                    cloud_ref=conv_utils.get_object_ref(cloud_name, 'cloud'),
                    tenant_ref=conv_utils.get_object_ref(tenant, 'tenant')

                )
                tier1_lr = ''
                for ref in nsx_lb_config['LBServices']:
                    if lb_vs['lb_service_path'] == ref['path']:
                        tier1_lr = ref.get('connectivity_path', None)

                if lb_vs.get('ip_address'):
                    vip = dict(
                        name=name + '-vsvip',
                        tier1_lr=tier1_lr,
                        cloud_ref=conv_utils.get_object_ref(cloud_name, 'cloud'),
                        vip=[
                            dict(
                                vip_id = "1",
                                ip_address=dict(
                                    addr=lb_vs.get('ip_address'),
                                    type='V4'
                                )
                            )
                        ]

                    )
                    alb_config['VsVip'].append(vip)
                    vsvip_ref = '/api/vsvip/?name=%s&cloud=%s' % (name + '-vsvip', cloud_name)
                    alb_vs['vsvip_ref'] = vsvip_ref
                alb_vs['services'] = [
                    dict(
                        port=int(lb_vs.get('ports')[0]),
                        enable_ssl=False
                    )]
                skipped = [val for val in lb_vs.keys()
                           if val not in self.supported_attr]
                na_list = [val for val in lb_vs.keys()
                           if val in self.common_na_attr or val in self.VS_na_attr]
                if segroup:
                    segroup_ref = conv_utils.get_object_ref(
                        segroup, 'serviceenginegroup', "admin",
                        cloud_name=cloud_name)
                    alb_vs['se_group_ref'] = segroup_ref

                if lb_vs.get('application_profile_path'):
                    profile_path = lb_vs.get('application_profile_path')
                    profile_name = profile_path.split('/')[-1]
                    if prefix:
                        profile_name=prefix+"-"+profile_name
                    profile_type="network"
                    for profile in alb_config["ApplicationProfile"]:
                        if profile["name"] == profile_name:
                            profile_type="application"
                    app_profile_ref = self.get_vs_app_profile_ref(alb_config['ApplicationProfile'],
                                                                          profile_name, self.object_merge_check,
                                                                          self.merge_object_mapping, profile_type)
                    if app_profile_ref.__contains__("networkprofile"):
                        alb_vs['network_profile_ref'] = app_profile_ref
                        alb_vs['application_profile_ref'] = conv_utils.get_object_ref("System-L4-Application", 'applicationprofile',
                                                                                      tenant="admin")
                    else:
                        alb_vs['application_profile_ref'] = app_profile_ref
                        alb_vs['network_profile_ref'] = conv_utils.get_object_ref("System-TCP-Proxy", 'networkprofile',
                                                                                      tenant="admin")
                if lb_vs.get('max_concurrent_connections'):
                    alb_vs['performance_limits'] = dict(
                        max_concurrent_connections=lb_vs.get('max_concurrent_connections')
                    )
                if lb_vs.get('client_ssl_profile_binding'):
                    client_ssl =  lb_vs.get('client_ssl_profile_binding')
                    if client_ssl.get('ssl_profile_path'):
                        ssl_ref = client_ssl['ssl_profile_path'].split('/')[-1]
                        if prefix:
                            ssl_ref = prefix + '-' + ssl_ref
                        alb_vs['ssl_profile_ref'] = '/api/sslprofile/?tenant=admin&name=' + ssl_ref
                    if client_ssl.get('default_certificate_path', None):
                        alb_vs['services'][0]["enable_ssl"] = True
                        ca_cert_obj = self.update_ca_cert_obj(name, alb_config, [], "admin", prefix)
                        ssl_key_cert_refs = []
                        ssl_key_cert_refs.append("/api/sslkeyandcertificate/?tenant=admin&name=" + ca_cert_obj.get("name"))
                        alb_vs["ssl_key_and_certificate_refs"] = list(set(ssl_key_cert_refs))
                        converted_alb_ssl_certs.append(ca_cert_obj)

                    skipped = [val for val in skipped
                               if val not in self.client_ssl_attr]
                if lb_vs.get('pool_path'):
                    pool_ref = lb_vs.get('pool_path')
                    pool_name = pool_ref.split('/')[-1]
                    if prefix:
                        pool_name = prefix + '-' + pool_name

                    alb_vs['pool_ref']  = conv_utils.get_object_ref(
                        pool_name, 'pool', tenant="admin", cloud_name=cloud_name)
                    # alb_vs['pool_ref'] = '/api/pool/?tenant=admin&name=' + pool_name
                    if lb_vs.get('server_ssl_profile_binding'):
                        self.update_pool_with_ssl(alb_config, lb_vs, pool_name, self.object_merge_check,
                                                  self.merge_object_mapping, prefix, converted_alb_ssl_certs)
                        skipped = [val for val in skipped
                                   if val not in self.server_ssl_attr]
                if lb_vs.get('lb_persistence_profile_path'):
                    self.update_pool_with_persistence(alb_config['Pool'], lb_vs,
                                                      pool_name, self.object_merge_check, self.merge_object_mapping,
                                                      prefix)

                for pool in alb_config['Pool']:
                    if pool.get('name') == pool_name:
                        if lb_vs.get('default_pool_member_ports'):
                            pool['default_port'] = int(lb_vs['default_pool_member_ports'][0])
                        pool['tier1_lr'] = tier1_lr
                indirect = []
                u_ignore = []
                ignore_for_defaults = {}
                conv_status = conv_utils.get_conv_status(
                    skipped, indirect, ignore_for_defaults, nsx_lb_config['LbVirtualServers'],
                    u_ignore, na_list)
                conv_utils.add_conv_status('virtualservice', None, alb_vs['name'], conv_status,
                                           alb_vs)
                alb_config['VirtualService'].append(alb_vs)

                msg = "Server conversion started..."
                conv_utils.print_progress_bar(progressbar_count, total_size, msg,
                                              prefix='Progress', suffix='')
                if len(conv_status['skipped']) > 0:
                    LOG.debug('[VirtualService] Skipped Attribute {}:{}'.format(lb_vs['display_name'],
                                                                                conv_status['skipped']))

                LOG.info('[VirtualService] Migration completed for HM {}'.format(lb_vs['display_name']))
            except Exception as e:
                LOG.error("[VirtualService] Failed to convert VirtualService: {}".format(e))
                update_count('error')
                LOG.error("[VirtualServer] Failed to convert Monitor: %s" % lb_vs['display_name'],
                          exc_info=True)
                conv_utils.add_status_row('virtual', None, lb_vs['display_name'],
                                          conv_const.STATUS_ERROR)
        for cert in converted_alb_ssl_certs:
            indirect = []
            u_ignore = []
            ignore_for_defaults = {}
            conv_status = conv_utils.get_conv_status(
                [], indirect, ignore_for_defaults, [],
                u_ignore, [])
            conv_utils.add_conv_status('ssl_key_and_certificate', None, cert['name'], conv_status,
                                       [{"ssl_cert_key":cert}])


    def update_pool_with_ssl(self, alb_config, lb_vs, pool_name, object_merge_check, merge_object_mapping, prefix, converted_alb_ssl_certs):
        for pool in alb_config['Pool']:
            if pool.get('name') == pool_name:
                server_ssl = lb_vs['server_ssl_profile_binding']
                if server_ssl.get('ssl_profile_path'):
                    ssl_ref = server_ssl['ssl_profile_path'].split('/')[-1]
                    if prefix:
                        ssl_ref = prefix + '-' + ssl_ref
                    if object_merge_check:
                        ssl_name = merge_object_mapping['ssl_profile'].get(ssl_ref)
                        if ssl_name:
                            ssl_ref = ssl_name
                    pool['ssl_profile_ref'] = '/api/sslprofile/?tenant=admin&name=' + ssl_ref
                if server_ssl.get('client_certificate_path', None):
                    ca_cert_obj = self.update_ca_cert_obj(pool_name, alb_config, [], "admin", prefix)
                    pool["ssl_key_and_certificate_ref"] = "/api/sslkeyandcertificate/?tenant=admin&name=" + ca_cert_obj.get("name")
                    converted_alb_ssl_certs.append(ca_cert_obj)

    def update_pool_with_persistence(self, alb_pool_config, lb_vs, pool_name, object_merge_check, merge_object_mapping,
                                     prefix):
        for pool in alb_pool_config:
            if pool.get('name') == pool_name and lb_vs.get('lb_persistence_profile_path', None):
                if prefix:
                    persistence_name = prefix + '-' + lb_vs.get('lb_persistence_profile_path').split('/')[-1]
                else:
                    persistence_name = lb_vs.get('lb_persistence_profile_path').split('/')[-1]
                pool['persistence_profile_ref'] = '/api/applicationpersistenceprofile/?tenant=admin&name=' + persistence_name

    def get_vs_app_profile_ref(self, alb_profile_config, profile_name, object_merge_check,
                               merge_object_mapping, profile_type):
        if object_merge_check:
            app_profile_merge_name = merge_object_mapping['app_profile'].get(profile_name)
            if app_profile_merge_name:
                profile_name = app_profile_merge_name
                return '/api/applicationprofile/?tenant=admin&name=' + profile_name
            np_prodile_merge_name=merge_object_mapping['network_profile'].get(profile_name)
            if np_prodile_merge_name:
                profile_name=np_prodile_merge_name
                return '/api/networkprofile/?tenant=admin&name=' + profile_name
        if profile_type == "application":
            return '/api/applicationprofile/?tenant=admin&name=' + profile_name
        return '/api/networkprofile/?tenant=admin&name=' + profile_name

    def update_ca_cert_obj(self, name, avi_config, converted_objs, tenant, prefix, cert_type='SSL_CERTIFICATE_TYPE_CA', ca_cert=None):
        """
        This method create the certs if certificate not present at location
        it create placeholder certificate.
        :return:
        """

        cert_name = [cert['name'] for cert in avi_config.get("SSLKeyAndCertificate", [])
                     if cert['name'].__contains__(name) and cert['type'] == cert_type]

        if cert_name:
            LOG.warning(
                'SSL ca cert is already exist')

            for cert in avi_config.get("SSLKeyAndCertificate", []):
                if cert['name'].__contains__(name) and cert['type'] == cert_type:
                    return cert
            return None

        if not ca_cert:
            key, ca_cert = conv_utils.create_self_signed_cert()
            name = '%s-%s' % (name, final.PLACE_HOLDER_STR)
            LOG.warning('Create self cerificate and key for : %s' % name)

        ssl_kc_obj = None

        if ca_cert:
            cert = {"certificate": ca_cert if type(ca_cert) == str else ca_cert.decode()}
            ssl_kc_obj = {
                'name': name,
                'tenant_ref': conv_utils.get_object_ref(tenant, 'tenant'),
                'key': key if type(key) == str else key.decode(),
                'certificate': cert,
                'type': 'SSL_CERTIFICATE_TYPE_VIRTUALSERVICE'
            }
            LOG.info('Added new ca certificate for %s' % name)
        if ssl_kc_obj and self.object_merge_check:
            if final.PLACE_HOLDER_STR not in ssl_kc_obj['name']:
                conv_utils.update_skip_duplicates(
                    ssl_kc_obj, avi_config['SSLKeyAndCertificate'],
                    'ssl_cert_key', converted_objs, name, None,
                    self.merge_object_mapping, None, prefix,
                    self.sys_dict['SSLKeyAndCertificate'])
            else:
                converted_objs.append({'ssl_cert_key': ssl_kc_obj})
                avi_config['SSLKeyAndCertificate'].append(ssl_kc_obj)
            self.certkey_count += 1
        else:
            converted_objs.append({'ssl_cert_key': ssl_kc_obj})
            avi_config['SSLKeyAndCertificate'].append(ssl_kc_obj)
        return ssl_kc_obj