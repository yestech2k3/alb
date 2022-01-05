import logging
import os

from avi.migrationtools.avi_migration_utils import update_count
from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil
import avi.migrationtools.nsxt_converter.converter_constants as final
import avi.migrationtools.nsxt_converter.converter_constants as conv_const


LOG = logging.getLogger(__name__)

conv_utils = NsxtConvUtil()
class SslProfileConfigConv(object):
    def __init__(self, nsxt_profile_attributes):
        """

        """
        self.supported_client_ssl_attributes = nsxt_profile_attributes['SSLProfile_Client_Supported_Attributes']
        self.supported_server_ssl_attributes = nsxt_profile_attributes['SSLProfile_Server_Supported_Attributes']
        self.common_na_attr = nsxt_profile_attributes['Common_Na_List']
        #TODO
        self.object_merge_check = None
        self.certkey_count = 0


    def convert(self, alb_config, nsx_lb_config, prefix):
        alb_config["SSLProfile"] = []
        if nsx_lb_config.get('LbClientSslProfiles'):
            progressbar_count = 0
            total_size = len(nsx_lb_config['LbClientSslProfiles'])
            print("\nConverting Client SSL Profile ...")
            LOG.info('[SSL-PROFILE] Converting Profiles...')

            for lb_ssl in nsx_lb_config["LbClientSslProfiles"]:
                try:
                    LOG.info('[SSL-PROFILE] Migration started for AP {}'.format(lb_ssl['display_name']))
                    skipped = [val for val in lb_ssl.keys()
                               if val not in self.supported_client_ssl_attributes]
                    na_list = [val for val in lb_ssl.keys()
                               if val in self.common_na_attr]

                    progressbar_count += 1
                    name = lb_ssl.get('display_name')
                    if prefix:
                        name = prefix + '-' + name
                    alb_ssl = dict(
                        name = name,
                    )
                    if lb_ssl.get("session_cache_enabled"):
                        alb_ssl['enable_ssl_session_reuse'] = lb_ssl['session_cache_enabled']
                    if lb_ssl.get("session_cache_timeout"):
                        alb_ssl['ssl_session_timeout'] = lb_ssl['session_cache_timeout']

                    if lb_ssl.get("ciphers"):
                        alb_ssl['accepted_ciphers'] = ":".join(lb_ssl['ciphers'])

                    if lb_ssl.get("protocols"):
                        self.convert_protocols(lb_ssl['protocols'], alb_ssl)

                    indirect = []
                    u_ignore = []
                    ignore_for_defaults = {}
                    conv_status = conv_utils.get_conv_status(
                        skipped, indirect, ignore_for_defaults, nsx_lb_config['LbMonitorProfiles'],
                        u_ignore, na_list)

                    conv_utils.add_conv_status('sslprofile', lb_ssl['resource_type'], alb_ssl['name'], conv_status,
                                               [{'ssl_profile': alb_ssl}])

                    alb_config['SSLProfile'].append(alb_ssl)
                    msg = "SSLProfile conversion started..."
                    conv_utils.print_progress_bar(progressbar_count, total_size, msg,
                                                  prefix='Progress', suffix='')
                    # time.sleep(1)
                    if len(conv_status['skipped']) > 0:
                        LOG.debug(
                            '[SSL-PROFILE] Skipped Attribute {}:{}'.format(lb_ssl['display_name'], conv_status['skipped']))

                    LOG.info('[SSL-PROFILE] Migration completed for HM {}'.format(lb_ssl['display_name']))

                except:
                    update_count('error')
                    LOG.error("[SSL-PROFILE] Failed to convert Client SSLProfile: %s" % lb_ssl['display_name'],
                              exc_info=True)
                    conv_utils.add_status_row('sslprofile', None, lb_ssl['display_name'],
                                              conv_const.STATUS_ERROR)
        if nsx_lb_config.get('LbServerSslProfiles'):
            progressbar_count = 0
            total_size = len(nsx_lb_config['LbServerSslProfiles'])
            print("\nConverting Server SSL Profile ...")
            LOG.info('[SSL-PROFILE] Converting Client SSL Profiles...')

            for lb_ssl in nsx_lb_config["LbServerSslProfiles"]:
                try:
                    LOG.info('[SSL-PROFILE] Migration started for AP {}'.format(lb_ssl['display_name']))
                    skipped = [val for val in lb_ssl.keys()
                               if val not in self.supported_client_ssl_attributes]
                    na_list = [val for val in lb_ssl.keys()
                               if val in self.common_na_attr]
                    progressbar_count += 1
                    name = lb_ssl.get('display_name')
                    if prefix:
                        name = prefix + '-' + name
                    alb_ssl = dict(
                        name = name,
                    )
                    if lb_ssl.get("ciphers"):
                        alb_ssl['accepted_ciphers'] = ":".join(lb_ssl['ciphers'])
                    if lb_ssl.get("protocols"):
                        self.convert_protocols(lb_ssl['protocols'], alb_ssl)

                    indirect = []
                    u_ignore = []
                    ignore_for_defaults = {}
                    conv_status = conv_utils.get_conv_status(
                        skipped, indirect, ignore_for_defaults, nsx_lb_config['LbMonitorProfiles'],
                        u_ignore, na_list)

                    conv_utils.add_conv_status('sslprofile', lb_ssl['resource_type'], alb_ssl['name'], conv_status,
                                               [{'ssl_profile': alb_ssl}])

                    alb_config['SSLProfile'].append(alb_ssl)
                    msg = "SSLProfile conversion started..."
                    conv_utils.print_progress_bar(progressbar_count, total_size, msg,
                                                  prefix='Progress', suffix='')
                    # time.sleep(1)
                    if len(conv_status['skipped']) > 0:
                        LOG.debug(
                            '[SSL-PROFILE] Skipped Attribute {}:{}'.format(lb_ssl['display_name'],
                                                                           conv_status['skipped']))

                    LOG.info('[SSL-PROFILE] Migration completed for HM {}'.format(lb_ssl['display_name']))
                except:
                    update_count('error')
                    LOG.error("[SSL-PROFILE] Failed to convert Server Side SSLProfile: %s" % lb_ssl['display_name'],
                              exc_info=True)
                    conv_utils.add_status_row('sslprofile', None, lb_ssl['display_name'],
                                              conv_const.STATUS_ERROR)
        alb_config['SSLKeyAndCertificate'] = list()
        self.update_ca_cert_obj("avi-self-sighned-certificate", alb_config, [], "admin")


    def update_key_cert_obj(self, name, key_file_name, cert_file_name,
                            input_dir, tenant, avi_config, converted_objs,
                            default_profile_name, key_and_cert_mapping_list,
                            merge_object_mapping, sys_dict):
        """
        This method create the certs if certificate not present at location
        it create placeholder certificate.
        :param name: name of certificate.
        :param key_file_name: name of keyfile of cert
        :param cert_file_name: name of cert file
        :param input_dir: location of cert and key
        :param tenant: tenant name
        :param avi_config: converted avi config dict
        :param converted_objs: list of converted object profile
        :param default_profile_name: name of default profile name.
        :param key_and_cert_mapping_list: list of key and cert
        :param merge_object_mapping: merged object dict for merging objects
        :param sys_dict: baseline objects
        :return:
        """

        cert_name = [cert['name'] for cert in key_and_cert_mapping_list if
                     cert['key_file_name'] == key_file_name and
                     cert['cert_file_name'] == cert_file_name]

        if cert_name:
            LOG.warning(
                'SSL key and Certificate is already exist for %s and %s is %s' %
                (key_file_name, cert_file_name, cert_name[0]))
            return
        folder_path = input_dir + os.path.sep
        key = None
        cert = None
        if key_file_name and cert_file_name:
            # Removed / from key_file_name to get name of file.
            if '/' in key_file_name:
                key_file_name = key_file_name.split('/')[-1]
            # Removed / from cert_file_name to get name of file.
            if '/' in cert_file_name:
                cert_file_name = cert_file_name.split('/')[-1]
            key = conv_utils.upload_file(folder_path + key_file_name)
            cert = conv_utils.upload_file(folder_path + cert_file_name)

        is_key_protected = False
        if key:
            # Check kay is passphrase protected or not
            is_key_protected = conv_utils.is_certificate_key_protected(
                input_dir + os.path.sep + key_file_name)

        if cert and key:
            # Flag to check expiry date of certificate. if expired then
            # create placeholder certificate.
            if not conv_utils.check_certificate_expiry(input_dir,
                                                    cert_file_name):
                cert, key = None, None

        key_passphrase = None
        # Get the key passphrase for key_file
        if is_key_protected and self.f5_passphrase_keys:
            key_passphrase = self.f5_passphrase_keys.get(key_file_name, None)

        if is_key_protected and not key_passphrase:
            key = None

        if not key or not cert:
            key, cert = conv_utils.create_self_signed_cert()
            name = '%s-%s' % (name, final.PLACE_HOLDER_STR)
            LOG.warning('Create self cerificate and key for : %s' % name)

        ssl_kc_obj = None
        if tenant == None:
            tenant = 'admin'
        if key and cert:
            cert = {"certificate": cert if type(cert) == str else cert.decode()}
            ssl_kc_obj = {
                'name': name,
                'tenant_ref': conv_utils.get_object_ref(tenant, 'tenant'),
                'key': key if type(key) == str else key.decode(),
                'certificate': cert,
                'type': 'SSL_CERTIFICATE_TYPE_VIRTUALSERVICE'
            }
        if key_passphrase:
            ssl_kc_obj['key_passphrase'] = key_passphrase
        if ssl_kc_obj:
            cert_obj = {'key_file_name': key_file_name,
                        'cert_file_name': cert_file_name,
                        'name': name
                        }
            key_and_cert_mapping_list.append(cert_obj)
            LOG.info('Added new SSL key and certificate for %s' % name)

        if ssl_kc_obj:
            if self.object_merge_check:
                if final.PLACE_HOLDER_STR not in ssl_kc_obj['name']:
                    conv_utils.update_skip_duplicates(ssl_kc_obj,
                        avi_config['SSLKeyAndCertificate'],'ssl_cert_key',
                        converted_objs, name, default_profile_name,
                        merge_object_mapping, None, self.prefix, sys_dict[
                        'SSLKeyAndCertificate'])
                else:
                    converted_objs.append({'ssl_cert_key': ssl_kc_obj})
                    avi_config['SSLKeyAndCertificate'].append(ssl_kc_obj)
                self.certkey_count += 1
            else:
                converted_objs.append({'ssl_cert_key': ssl_kc_obj})
                avi_config['SSLKeyAndCertificate'].append(ssl_kc_obj)

    def update_ca_cert_obj(self, name, avi_config, converted_objs, tenant):
        """
        This method create the certs if certificate not present at location
        it create placeholder certificate.
        :return:
        """

        cert_name = [cert['name'] for cert in avi_config.get("SSLKeyAndCertificate", [])
                     if cert['name'] == name and
                     cert['type'] == 'SSL_CERTIFICATE_TYPE_CA']

        if cert_name:
            LOG.warning(
                'SSL ca cert is already exist')
            return
        ca_cert = None
        if not ca_cert:
            key, ca_cert = conv_utils.create_self_signed_cert()
            name = '%s-%s' % (name, final.PLACE_HOLDER_STR)
            LOG.warning('Create self cerificate and key for : %s' % name)

        ca_cert_obj = None

        if ca_cert:
            cert = {"certificate": ca_cert if type(ca_cert) == str else ca_cert.decode()}
            ca_cert_obj = {
                'name': name,
                'tenant_ref': conv_utils.get_object_ref(tenant, 'tenant'),
                'certificate': cert,
                'type': 'SSL_CERTIFICATE_TYPE_CA'
            }
            LOG.info('Added new ca certificate for %s' % name)
        if ca_cert_obj and self.object_merge_check:
            # if final.PLACE_HOLDER_STR not in ca_cert_obj['name']:
            #     conv_utils.update_skip_duplicates(
            #         ca_cert_obj, avi_config['SSLKeyAndCertificate'],
            #         'ssl_cert_key', converted_objs, name, None,
            #         merge_object_mapping, None, self.prefix,
            #         sys_dict['SSLKeyAndCertificate'])
            # else:
            #     converted_objs.append({'ssl_cert_key': ca_cert_obj})
            #     avi_config['SSLKeyAndCertificate'].append(ca_cert_obj)
            self.certkey_count += 1
        else:
            converted_objs.append({'ssl_cert_key': ca_cert_obj})
            avi_config['SSLKeyAndCertificate'].append(ca_cert_obj)


    def convert_protocols(self, protocols, alb_ssl):
        accepted_version = dict(
            SSL_V2="",
            SSL_V3="SSL_VERSION_SSLV3",
            TLS_V1="SSL_VERSION_TLS1",
            TLS_V1_1="SSL_VERSION_TLS1_1",
            TLS_V1_2="SSL_VERSION_TLS1_2"

        )
        alb_ssl['accepted_versions'] = []

        for acc_ver in protocols:
            acc_version = dict(
                type=accepted_version[acc_ver]
            )
            alb_ssl['accepted_versions'].append(acc_version)
