'''Main dump file for video team.

version: 2.0
author : daviscao
date   : 20160428
config and driver dump_env_base.py
'''
# -*- coding: utf-8 -*-
import re
import dump_env_base
import os
import sys

def parse_cfgfile(dump_env_cfg):
    cfg_dict = dict()
    with open(dump_env_cfg,'r') as foo:
        cfg_lines = foo.readlines()
    if len(cfg_lines) == 0:
        print('Please prepare your dump_env_cfg.txt file ...')
        sys.exit(0)
    else:
        for each in cfg_lines:
            if re.match('\s*//.*',each):
                continue                            #jump the comment line
            elif re.search('=',each):
                each = re.sub('\s*//.*','',each)    #remove the comment at the end of the line
                each = each.strip()                 #remove the line-break
                each = re.sub('\s','',each)         #remove any space in the line
                key,value = re.split('=',each)
                if key == 'cmdidx_list':
                    cfg_dict[key] = list()
                    for idxstr in re.split(',',value):
                        match = re.match('(\w+)-(\w+)',idxstr)
                        if match:
                            span_l = range(int(match.group(1)),int(match.group(2))+1)
                        else:
                            span_l = range(int(idxstr),int(idxstr)+1)
                        cfg_dict[key] += span_l
                else:
                    cfg_dict[key] = value
    cfg_dict['userinifile']         = cfg_dict['dump_cfg_path']+os.sep+cfg_dict['userinifile']
    cfg_dict['userbatfile']         = cfg_dict['dump_cfg_path']+os.sep+cfg_dict['userbatfile']
    cfg_dict['basic_binary_path']   = cfg_dict['dump_path']+os.sep+cfg_dict['binary_num']
    cfg_dict['abt_binary_path']     = cfg_dict['abt_path']+os.sep+cfg_dict['binary_num']

    for each in cfg_dict:
        print(each,cfg_dict[each])
        try:
            if re.search(r'\\',cfg_dict[each]):
                if not os.path.exists(cfg_dict[each]):
                    print("    *E: the path '%s' does not exists ...\n"%cfg_dict[each])
        except:
            pass
    return cfg_dict

if __name__ == '__main__':
    stdout_old = sys.stdout
    with open('dump.log','w') as log:
        sys.stdout = log
        print('\n****************** parse the config *********************\n')
        dump_env_cfg = 'dump_env_cfg.txt'
        dump_cfg_dict = parse_cfgfile(dump_env_cfg)
        print('\n******************* start dump vector *******************\n')
    sys.stdout = stdout_old
    dump_inst = dump_env_base.dump_env(dump_cfg_dict)
    dump_inst.kickoff_dumpenv()
