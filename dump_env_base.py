'''Basic dump env for video team.

version: 2.0
author : daviscao
date   : 20160427
the basic chass tool to dump a list command batch in special format
'''
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import time
import re


class dump_env:
    def __init__(self):
        self.basic_binary_path = basic_binary_path
        self.abt_binary_path   = abt_binary_path
        self.usermodedrivername = usermodedrivername
        self.datmode = datmode
        self.result_path = result_path
        self.userinifile = userinifile
        self.userbatfile = userbatfile
        self.runvat_path = None
        self.ininame = ininame
        self.cmdidx_list = cmdidx_list
        self.run_env_path = os.getcwd()

    def prepare_basic_binary(self):
        print('>> Enter the 1th step: prepare dump binary: %s ...' %self.basic_binary_path)
        if os.path.exists(self.abt_binary_path):
            if not os.path.exists(self.basic_binary_path):
                os.mkdir(self.basic_binary_path)
            if not os.path.exists(self.basic_binary_path+os.sep+'binary'):
                shutil.copytree(self.abt_binary_path+os.sep+'binary',
                                self.basic_binary_path+os.sep+'binary')
                os.chdir(self.basic_binary_path+os.sep+'binary')
                os.remove('igdumd32.dll')
                os.rename('S3DDX9L_32.dll',self.usermodedrivername)
                os.chdir(self.run_env_path)
            else:
                print("     '%s' exists already, jump this step" %self.basic_binary_path)
        else:
            print("     *Error: check your binary '%s' on the server" %self.abt_binary_path)

    def prepare_cteini(self):
        time.sleep(2)
        print('>> Enter the 2th step: prepare cte.ini and VideoVectorCut.ini ...')
        with open(r'C:\CTEDump.ini','w') as foo:
            foo.write('DUMP ON'+'\n')
            foo.write('PATH '+self.result_path+'\n')
            foo.write('DATMODE '+self.datmode+'\n')
            foo.write('CTECompare ON'+'\n')
            foo.write('CTEPresent ON'+'\n')
            foo.write('DISASMDMA OFF'+'\n')
        with open(r'C:\VideoVectorCut.ini','w') as foo:
            foo.write('MODE 0'+'\n')
            foo.write('FRAME 0'+'\n') #any will be OK

    def prepare_rundir(self):
        print('>> Enter the 3th step: prepare run vat dir and its .ini file ...')
        rundate = time.strftime('%Y%m%d',time.localtime(time.time()))
        i = 1
        while True:
            if os.path.exists(self.basic_binary_path+os.sep+rundate+'_'+str(i)):
                i = i+1
            else:
                self.runvat_path = self.basic_binary_path+os.sep+rundate+'_'+str(i)
                shutil.copytree(self.basic_binary_path+os.sep+'binary',self.runvat_path)
                break
            
        os.remove(self.runvat_path+os.sep+self.ininame)
        shutil.copy(self.userinifile,self.runvat_path+os.sep+self.ininame)

        print('     '+self.runvat_path)
        print('     '+self.userinifile)
####
    def start_dump_batch(self):
        with open(self.userbatfile,'r') as bat:
            batlines = bat.readlines()
        print(self.cmdidx_list)
        for idx in self.cmdidx_list:
            print('     cmd idx : %d'%idx)
            cmdline = batlines[idx - 1]
            cmdline = cmdline.replace('\n','')
            print('       >> '+cmdline)
            self.start_dump_onecmd(cmdline)

    def start_dump_onecmd(self,cmdline):
        key,name,cmd = re.split('\s*=>\s*',cmdline)
        dump_results_l = os.listdir(self.result_path)
        if key+'_'+name in dump_results_l:#no need to dump
            print('rename jump')
        elif name in dump_results_l:#dumping or un-rename
            print('dumping jump')
        else:
            try:
                os.chdir(self.runvat_path)
                os.system(cmd)
                print(key,name,cmd)
            except:
                pass
            finally:
                dump_result = self.result_path+os.sep+name
                if os.path.exists(dump_result):
                    os.rename(dump_result,self.result_path+os.sep+key+'_'+name)
    ####
    def dump_prepare_phase(self):
        self.prepare_basic_binary()
        self.prepare_cteini()
        self.prepare_rundir()
    def dump_run_phase(self):
        print('>> Enter the 4th step: run command in the list ...')
        self.start_dump_batch()
    #### main function ####
    def kickoff_dumpenv(self):
        self.dump_prepare_phase()
        self.dump_run_phase()
    
if __name__ == '__main__':
    #dump_env_cfg = 'dump_env_cfg.txt'
    basic_binary_path = r'D:\hw\CHX001\231981'
    abt_binary_path = r'Y:\CHX001\231981'
    usermodedrivername = 'igdumdim32.dll'
    datmode = 'BIN'
    result_path = r'E:\hw\CHX001\dump'

    userinifile = r'D:\hw\CHX001\dump_cfg\Excalibur.ini'
    userbatfile = r'D:\hw\CHX001\dump_cfg\bat.txt'
    ininame = 'Excalibur.ini'
    dump_inst = dump_env()
    dump_inst.kickoff_dumpenv()
