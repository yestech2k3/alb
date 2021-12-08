import json
import logging
import os

import avi.migrationtools.nsxt_converter.converter_constants as conv_const
from avi.migrationtools.avi_migration_utils import update_count
from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil
from avi.migrationtools.nsxt_converter.monitor_converter \
    import MonitorConfigConv
from avi.migrationtools.nsxt_converter.nsxt_util import NSXUtil
from avi.migrationtools.nsxt_converter.pools_converter import PoolConfigConv
from avi.migrationtools.nsxt_converter.profile_converter \
    import ProfileConfigConv
from avi.migrationtools.nsxt_converter.ssl_profile_converter \
    import SslProfileConfigConv

LOG = logging.getLogger(__name__)


conv_utils = NsxtConvUtil()


def convert(nsx_ip, nsx_un, nsx_pw, nsx_port, output_dir, cloud_name, prefix):
    # load the yaml file attribute in nsxt_attributes.
    nsxt_attributes = conv_const.init("11")

    nsx_util = NSXUtil(nsx_un, nsx_pw, nsx_ip, nsx_port)
    nsx_lb_config = nsx_util.get_nsx_config()
    input_path = output_dir + os.path.sep + nsx_ip + os.path.sep + "input"
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    input_config = input_path + os.path.sep + "config.json"
    with open(input_config, "w", encoding='utf-8') as text_file:
        json.dump(nsx_lb_config, text_file, indent=4)

    alb_config = dict()  # Result Config

    try:
        monitor_converter = MonitorConfigConv(nsxt_attributes)
        monitor_converter.convert(alb_config, nsx_lb_config, prefix)

        pool_converter = PoolConfigConv(nsxt_attributes)
        pool_converter.convert(alb_config, nsx_lb_config, cloud_name, prefix)

        profile_converter = ProfileConfigConv(nsxt_attributes)
        profile_converter.convert(alb_config, nsx_lb_config, prefix)

        #TO-DO
        # ssl_profile_converter = SslProfileConfigConv(nsxt_attributes)
        # ssl_profile_converter.convert(alb_config, nsx_lb_config, prefix)
    except:
        update_count('warning')
        LOG.error("Conversion error", exc_info=True)

    output_path = output_dir + os.path.sep + nsx_ip + os.path.sep + "output"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_config = output_path + os.path.sep + "avi_config.json"
    with open(output_config, "w", encoding='utf-8') as text_file:
        json.dump(alb_config, text_file, indent=4)

    # Add nsxt converter status report in xslx report
    conv_utils.add_complete_conv_status(
        output_path, alb_config, "nsxt-report", False)

    for key in alb_config:
        if key != 'META':
            LOG.info('Total Objects of %s : %s' % (key, len(
                alb_config[key])))
            print('Total Objects of %s : %s' % (key, len(
                alb_config[key])))
    return alb_config

