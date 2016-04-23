'''Main dump file:dump_main.py.

author : daviscao@zhaoxin.com
date   : 2016.4.15
config and driver dump_env_base.py'''

# -*- coding: utf-8 -*-
import re
import dump_env_base


if __name__ == '__main__':
    dump_env_cfg = 'dump_env_cfg.txt'
    cfg_dict = dict()
    with open(dump_env_cfg,'r') as foo:
        cfg_lines = foo.readlines()
    if len(cfg_lines) == 0:
        print('Please prepare your dump_env_cfg.txt file ...')
        input('print any key to continue ...')
    else:
        for each in cfg_lines:
            if re.search('=',each):
                each = each.strip()
                each = re.sub(' ','',each)
                key,value = re.split('=',each)
                if key == 'cmdidx_list':
                    cfg_dict[key] = map(int,value.split(','))
                else:
                    cfg_dict[key] = value

    dump_env_inst = dump_env_base.dump_env(project            = cfg_dict['project'],
                                           binary             = cfg_dict['binary'],
                                           batch              = cfg_dict['batch'],
                                           inifile            = cfg_dict['inifile'],
                                           cmdidx_list        = cfg_dict['cmdidx_list'],
                                           result_path        = cfg_dict['result_path'],
                                           datmode            = cfg_dict['datmode'],
                                           usermodedrivername = cfg_dict['usermodedrivername'])
    dump_env_inst.kickoff_dumpenv()
    
