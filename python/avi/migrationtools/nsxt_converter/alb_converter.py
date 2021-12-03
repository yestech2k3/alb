import argparse
import json
import os
from pprint import PrettyPrinter
import avi.migrationtools.nsxt_converter.converter_constants as conv_const


# SUPPORTED_ALB_OBJECTS = ['VirtualService']



class ALBConverter:
    def __init__(self, args):
        '''

        '''
        self.avi_config_file = args.avi_config_file
        self.output_file_path = args.output_file_path if args.output_file_path \
            else 'output-alb'



    def convert(self):

        if not os.path.exists(self.output_file_path):
            os.mkdir(self.output_file_path)
        output_dir = os.path.normpath(self.output_file_path)
        input_path = output_dir + os.path.sep + os.path.sep + "input-alb"
        if not os.path.exists(input_path):
            os.makedirs(input_path)
        input_config = input_path + os.path.sep + "config.json"
        with open(self.avi_config_file, "r") as read_file:
            avi_config = json.load(read_file)

        with open(input_config, "w", encoding='utf-8') as text_file:
            json.dump(avi_config, text_file, indent=4)

        alb_config = self.convert_to_alb(avi_config)
        pp = PrettyPrinter()
        pp.pprint(alb_config)

        output_path = output_dir + os.path.sep + os.path.sep + "output-alb"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_config = output_path + os.path.sep + "alb_config.json"
        with open(output_config, "w", encoding='utf-8') as text_file:
            json.dump(alb_config, text_file, indent=4)

    def convert_to_alb(self, avi_config):
        alb_config = dict()
        for key in avi_config.keys():
            if key in SUPPORTED_ALB_OBJECTS:
                config = []
                supported_obj = avi_config[key]
                for obj in supported_obj:
                    data = self.recursive_items(obj, {})
                    config.append(data)
                alb_config[key] = config
        return alb_config

    def recursive_items(self, obj, data):

        for k, v in obj.items():
            if k not in nsxt_attributes['NOT_APPLICABLE']:
                if type(v) is dict:
                    data[k] = self.recursive_items(v, {})
                elif not k.endswith("_refs") and type(v) is list:
                    tmp = []
                    for iter_over_obj in v:
                        if type(iter_over_obj) is dict:
                            tmp.append(self.recursive_items(iter_over_obj, {}))
                        else:
                            tmp.append(iter_over_obj)
                    data[k] = tmp
                elif k in nsxt_attributes['REPLACE_KEYS']:

                    if k == nsxt_attributes['REPLACE_KEYS'][0]:
                        data['display_name'] = v
                        data['id'] = v
                    if k == nsxt_attributes['REPLACE_KEYS'][0]:
                        data['cloud_name'] = v.split("name=")[1]
                    if k == nsxt_attributes['REPLACE_KEYS[2]']:
                        data['vrf_name'] = v.split("name=")[1].split("&")[0]
                    if k == nsxt_attributes['REPLACE_KEYS'][3]:
                        data['vrf_context_name'] = v.split("name=")[1].split("&")[0]
                    if k == nsxt_attributes['REPLACE_KEYS'][4]:
                        data["tier1_path"] = v
                elif k.endswith("_ref"):
                    if v.split('/')[2] not in nsxt_attributes['albObjectType'].keys():
                        continue
                    object_type = nsxt_attributes['albObjectType'][v.split('/')[2]]
                    data[k.replace("_ref", "_path")] = "/infra/" + object_type + "/" + v.split("name=")[1]
                elif k.endswith("_refs"):
                    list_of_paths = [ "/infra/" + nsxt_attributes['albObjectType'][data.split('/')[2]] + "/" + data.split("name=")[1] for data in v ]
                    data[k.replace("_refs", "_paths")] = list_of_paths
                else:
                    data[k] = v
        return data


if __name__ == "__main__":
    HELP_STR = '''
       Converts AVI Config to ALB config.
       Example to convert AVI config file to ALB config json:
            alb_converter.py -f tmp_exported_config.json
       '''

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=(HELP_STR))

    # Added args for baseline profile json file
    parser.add_argument('-f', '--avi_config_file',
                        help='absolute path for avi config file')
    parser.add_argument('-o', '--output_file_path',
                        help='Folder path for output files to be created in',
                        )

    args = parser.parse_args()
    nsxt_attributes = conv_const.init("11")

    alb_converter = ALBConverter(args)
    alb_converter.convert()