
import logging

from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil

LOG = logging.getLogger(__name__)

conv_utils = NsxtConvUtil()

class VSConfigConv(object):
    def __init__(self, nsxt_monitor_attributes):
        """

        """


    def convert(self, alb_config, nsx_lb_config, cloud_name, prefix):
        '''
        LBVirtualServer to Avi Config vs converter
        '''

        alb_config['VirtualService'] = list()
        alb_config['VsVip'] = []
        progressbar_count = 0
        total_size = len(nsx_lb_config['LbVirtualServer'])
        print("\nConverting Virtual Services ...")
        LOG.info('[Virtual Service ] Converting Services...')
        for lb_vs in nsx_lb_config['LbVirtualServer']:
            try:
                LOG.info('[Virtual Service] Migration started for VS {}'.format(lb_vs['display_name']))
                progressbar_count += 1
                name = lb_vs.get('display_name')
                if prefix:
                    name = prefix + '-' + name
                alb_vs = dict(
                    name = name ,
                    enabled = lb_vs.get('enabled'),
                    cloud_ref = conv_utils.get_object_ref(cloud_name, 'cloud')

                )
                pool_ref=lb_vs.get('poolPath')
                self.update_pool(alb_config, lb_vs, pool_ref)






    def update_pool(self,alb_config,lb_vs,pool_ref):
        pool_name=pool_ref.split('name=')[1].split('&')[0]
        pool_config = {pool for pool in alb_config['Pools'] if pool['name'] == pool_name}
        pool_config['persistence_profile_ref']=lb_vs.get('Lbpersistence')
        pool_config['ssl_profile_ref']=lb_vs.get('serverSslProfileBinding')
        pool_config['default_port'] = lb_vs.get('defaultPoolMemberPorts')










