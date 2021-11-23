from avi.migrationtools.nsxt_converter import conversion_util


def update_alb_type(lb_vs, alb_vs):
    alb_vs['url'], alb_vs['uuid'] = conversion_util.get_obj_url_uuid(lb_vs['path'], lb_vs['unique_id'])
    alb_vs['enabled'] = lb_vs['enabled']

    alb_vs['services']=dict(
        port=lb_vs['ports'][0]
        )
    alb_vs['pool_ref']=lb_vs['pool_path']
    alb_vs['application_profile_ref']=lb_vs['application_profile_path']
    alb_vs['ssl_profile_ref']=lb_vs.get('client_ssl_profile_binding')
    tenant = conversion_util.get_tenant_ref(alb_vs['url'])
    alb_vs['tenant_ref'] = conversion_util.get_object_ref('admin', 'tenant')

def convert(alb_config, nsx_lb_config,cloud_name):
    alb_config['VirtualService'] = list()
    alb_config['vsvip']=list()
    for lb_vs in nsx_lb_config['LBVirtualServers']:
        vsvip=dict(
            ip_address=dict(
                addr=lb_vs['ip_address'],
                type="V4"
        )
        )
        alb_vs = dict(
            name=lb_vs['display_name'],

        )

        update_alb_type(lb_vs, alb_vs)
        alb_vs['cloud_ref'] = conversion_util.get_object_ref(cloud_name, 'cloud')
        alb_config['VirtualService'].append(alb_vs)
        alb_config['vsvip'].append(vsvip)
