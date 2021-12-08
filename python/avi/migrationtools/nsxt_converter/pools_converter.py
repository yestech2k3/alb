import time

from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil

conv_utils = NsxtConvUtil()

class PoolConfigConv(object):
    def __init__(self, nsxt_pool_attributes):
        """
        :param nsxt_pool_attributes: Supported attributes for pool migration
        """
        self.supported_attr = nsxt_pool_attributes['Pool_supported_attr']
        self.server_attributes = nsxt_pool_attributes[
            'Pool_supported_attr_convert_servers_config']
        self.member_group_attr = nsxt_pool_attributes['Pool_supported_attr_convert_member_group']
        self.common_na_attr = nsxt_pool_attributes['Common_Na_List']


    def convert(self, alb_config, nsx_lb_config, cloud_name, prefix):
        '''
        LBPool to Avi Config pool converter
        '''
        alb_config['Pool'] = list()
        progressbar_count = 0

        total_size = len(nsx_lb_config['LbPools'])
        print("\nConverting Pools ...")
        for lb_pl in nsx_lb_config['LbPools']:
            progressbar_count += 1
            tenant, name = conv_utils.get_tenant_ref("admin")
            lb_type, name = self.get_name_type(lb_pl)

            na_list = [val for val in lb_pl.keys()
                       if val in self.common_na_attr]
            servers, member_skipped_config, skipped_servers , limits= \
                self.convert_servers_config(lb_pl.get("members", []))
            if prefix:
                name=prefix+"-"+name
            alb_pl = {
                'name': name,
                'servers': servers,
                'lb_algorithm': lb_type,
                'cloud_ref': conv_utils.get_object_ref(cloud_name, 'cloud')
            }

            if any(server.get("port") == None for server in servers):
                alb_pl.update({"use_service_port": "true"})
            alb_pl['tenant_ref'] = conv_utils.get_object_ref(tenant, 'tenant')

            if lb_pl.get("tcp_multiplexing_enabled"):
                #TO-DO - HANDLE In APPLICATION PROFILE
                #Need to set in Application profile
                pass

            if lb_pl.get("tcp_multiplexing_number"):
                alb_pl['conn_pool_properties'] = {
                    'upstream_connpool_server_max_cache': lb_pl.get('tcp_multiplexing_number')
                }
            if lb_pl.get('min_active_members'):
                alb_pl['min_servers_up'] = lb_pl.get('min_active_members')
            if limits.get('connection_limit', 0) > 0:
                alb_pl['max_concurrent_connections_per_server'] = \
                    limits['connection_limit']

            skipped_list_mg = []
            if lb_pl.get('member_group'):
                skipped_mg = [val for val in lb_pl.get('member_group').keys()
                           if val not in self.member_group_attr]
                skipped_list_mg.append({"skipped_mg": skipped_mg})
                if lb_pl['member_group'].get('group_path'):
                    alb_pl['nsx_securitygroup'] = [lb_pl.get('member_group').get('group_path')]
                if lb_pl['member_group'].get("port", None):
                    alb_pl['default_server_port'] = lb_pl['member_group'].get("port")
            if lb_pl.get("snat_translation"):
                # TO-DO - HANDLE In APPLICATION PROFILE
                # Need to set in Application profile
                 pass

            active_monitor_paths = lb_pl.get("active_monitor_paths", None)
            if active_monitor_paths:
                monitor_refs = []
                for lb_hm_path in active_monitor_paths:
                    ref=lb_hm_path.split("/lb-monitor-profiles/")[1]
                    if prefix:
                        ref=prefix+"-"+ref
                    monitor_refs.append("/api/healthmontior/?tenant=admin&name=" + ref)
                alb_pl["health_monitor_refs"] = list(set(monitor_refs))
            skipped = [val for val in lb_pl.keys()
                            if val not in self.supported_attr]

            indirect = []
            u_ignore = []
            ignore_for_defaults = {}
            if skipped_servers:
                skipped.append({"server": skipped_servers})
            if member_skipped_config:
                skipped.append(member_skipped_config)
            if skipped_list_mg:
                skipped.append(skipped_list_mg)

            conv_status = conv_utils.get_conv_status(
                skipped, indirect, ignore_for_defaults, nsx_lb_config['LbPools'],
                u_ignore, na_list)

            conv_utils.add_conv_status('pool', lb_type, alb_pl['name'], conv_status,
                                       [{'pool': alb_pl}])
            msg = "Pools conversion started..."
            conv_utils.print_progress_bar(progressbar_count, total_size, msg,
                                          prefix='Progress', suffix='')

            alb_config['Pool'].append(alb_pl)
            time.sleep(1)






    def get_name_type(self, lb_pl):
                """

                """
                type = ""
                if lb_pl['algorithm'] == 'ROUND_ROBIN' or lb_pl['algorithm'] == 'WEIGHTED_ROUND_ROBIN':
                    type = 'LB_ALGORITHM_ROUND_ROBIN'
                elif lb_pl['algorithm'] == 'LEAST_CONNECTION' or lb_pl['algorithm'] == 'WEIGHTED_LEAST_CONNECTION':
                    type = 'LB_ALGORITHM_LEAST_CONNECTION'
                elif lb_pl['algorithm'] == 'IP_HASH':
                    type = 'LB_ALGORITHM_CONSISTENT_HASH_SOURCE_IP_ADDRESS'
                return type, lb_pl['display_name']

    def convert_servers_config(self, servers_config):
        """

        """
        server_list = []
        skipped_list = []
        server_skipped = []
        connection_limit = []
        for member in servers_config:
            server_obj = {
                'ip': {
                    'addr': member['ip_address'],
                    'type': 'V4'
                },
                'description': member.get("display_name"),
            }

            if member.get("port", ""):
                server_obj['port'] = member.get("port")
            else:
                server_skipped.append(member.get("display_name"))

            if member.get("weight"):
                server_obj['ratio'] = member.get('weight')

            server_obj["enabled"]= False
            if member.get("admin_state") == "ENABLED":
                server_obj['enabled'] = True
            if member.get("max_concurrent_connections"):
                c_lim = int(member.get("max_concurrent_connections", '0'))
                if c_lim > 0:
                    connection_limit.append(c_lim)
            server_list.append(server_obj)
            skipped = [key for key in member.keys()
                       if key not in self.server_attributes]
            if skipped:
                skipped_list.append({member['display_name']: skipped})
        limits = dict()
        if connection_limit:
            limits['connection_limit'] = min(connection_limit)
        return server_list, skipped_list, server_skipped, limits
