import json
import logging
import os
import avi.migrationtools.nsxt_converter.converter_constants as conv_const
from avi.migrationtools.avi_migration_utils import update_count
from avi.migrationtools.nsxt_converter.conversion_util import NsxtConvUtil
from avi.migrationtools.nsxt_converter.monitor_converter \
    import MonitorConfigConv
from avi.migrationtools.nsxt_converter.nsxt_util import NSXUtil
import os
import json
from avi.migrationtools.nsxt_converter.alb_converter import ALBConverter
import avi.migrationtools.nsxt_converter.converter_constants as conv_const
from avi.migrationtools.nsxt_converter.pools_converter import PoolConfigConv
from avi.migrationtools.nsxt_converter.profile_converter \
    import ProfileConfigConv
from avi.migrationtools.nsxt_converter.ssl_profile_converter \
    import SslProfileConfigConv

LOG = logging.getLogger(__name__)


conv_utils = NsxtConvUtil()


def convert(nsx_lb_config,input_path, output_path, cloud_name, prefix,
            migrate_to):
    # load the yaml file attribute in nsxt_attributes.
    nsxt_attributes = conv_const.init()
    input_config = input_path + os.path.sep + "config.json"
    with open(input_config, "w", encoding='utf-8') as text_file:
        json.dump(nsx_lb_config, text_file, indent=4)

    avi_config_dict = dict()  # Result Config

    try:
        monitor_converter = MonitorConfigConv(nsxt_attributes)
        monitor_converter.convert(avi_config_dict, nsx_lb_config, prefix)

        pool_converter = PoolConfigConv(nsxt_attributes)
        pool_converter.convert(avi_config_dict, nsx_lb_config, cloud_name, prefix)

        profile_converter = ProfileConfigConv(nsxt_attributes)
        profile_converter.convert(avi_config_dict, nsx_lb_config, prefix)

        #TO-DO
        # ssl_profile_converter = SslProfileConfigConv(nsxt_attributes)
        # ssl_profile_converter.convert(alb_config, nsx_lb_config, prefix)

        # Validating the aviconfig after generation
        conv_utils.validation(avi_config_dict)
    except:
        update_count('warning')
        LOG.error("Conversion error", exc_info=True)

    output_config = output_path + os.path.sep + "avi_config.json"
    with open(output_config, "w", encoding='utf-8') as text_file:
        json.dump(avi_config_dict, text_file, indent=4)

    # Add nsxt converter status report in xslx report
    conv_utils.add_complete_conv_status(
        output_path, avi_config_dict, "nsxt-report", False)

    for key in avi_config_dict:
        if key != 'META':
            LOG.info('Total Objects of %s : %s' % (key, len(
                avi_config_dict[key])))
            print('Total Objects of %s : %s' % (key, len(
                avi_config_dict[key])))

    if migrate_to == 'NSX':
        alb_converter = ALBConverter(output_config, output_path)
        alb_converter.convert()

    return avi_config_dict

