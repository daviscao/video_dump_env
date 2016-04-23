'''Dump_env_base.py.

author : daviscao@zhaoxin.com
date   : 2016.4.15
the basic chass tool to dump a list command batch in special format'''
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import time
import re

class dump_env:
    def __init__(self,project,binary,batch,inifile,cmdidx_list,result_path,datmode,usermodedrivername):
        self.project     = project
        self.binary      = binary
        self.batch       = batch
        self.inifile     = inifile
        self.cmdidx_list = cmdidx_list
        self.result_path = result_path
        self.datmode     = datmode
        self.UMDN        = usermodedrivername

        self.runvat_dir  = ''
        self.runenv_path = os.getcwd()

        self.abt_binary_path  = r'Y:'+os.sep+self.project+os.sep+self.binary
        self.dump_binary_path = self.runenv_path + os.sep + self.binary
        #print (self.dump_binary_path)
#######
#######
    def prepare_dump_phase(self):
        print('>>>> Enter prepare dump phase >>>>')
        self.prepare_dump_binary()
        self.prepare_dump_cteini()
        self.prepare_dump_checkpath()
        self.prepare_dump_rundir()
    def prepare_dump_binary(self):
        if not os.path.exists(self.dump_binary_path):
            print('  >> enter the 1th step: prepare dump binary ...')
            if os.path.exists(self.abt_binary_path):
                shutil.copytree(self.abt_binary_path,self.dump_binary_path)
                os.chdir(self.dump_binary_path+os.sep+'binary')
                os.remove('igdumd32.dll')
                os.rename('S3DDX9L_32.dll',self.UMDN)
                os.chdir(self.runenv_path)
                #print('    >> plseas prepare your *.ini file ...')
                #sys.exit(0)
            else:
                print("  *ERROR: check your binary '%s' on the server" %self.abt_binary_path)
        else:
            print('  >> jump out the 1th step: prepare dump binary ...')
    def prepare_dump_cteini(self):
        time.sleep(1)
        print('  >> enter the 2th step: prepare cte.ini and VideoVectorCut.ini ...')
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
    def prepare_dump_checkpath(self):
        print('  >> enter the 3th step: check dump result path and config path ...')
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)
        if not os.path.exists(self.dump_binary_path+os.sep+'cfg_ini'):
            os.mkdir(self.dump_binary_path+os.sep+'cfg_ini')
        
        if not os.path.exists(self.dump_binary_path+os.sep+'cfg_bat'):
            os.mkdir(self.dump_binary_path+os.sep+'cfg_bat')
        if len(os.listdir(self.dump_binary_path+os.sep+'cfg_ini')) == 0:
            print('    >> please prepare the .ini file ...')
            sys.exit(0)
        if len(os.listdir(self.dump_binary_path+os.sep+'cfg_bat')) == 0:
            print('    >> please prepare the batch file ...')
            sys.exit(0)
    def prepare_dump_rundir(self):
        print('  >> enter the 4th step: prepare dump run dir ...')
        self.runvat_dir = time.strftime('%Y%m%d',time.localtime(time.time()))
        i = 1
        while True:
            #self.run_dir = self.dump_path+os.sep+self.binary+os.sep+self.run_dir+'_'+str(i)
            if os.path.exists(self.dump_binary_path+os.sep+self.runvat_dir+'_'+str(i)):
                i = i+1
            else:
                self.runvat_dir = self.dump_binary_path+os.sep+self.runvat_dir+'_'+str(i)
                shutil.copytree(self.dump_binary_path+os.sep+'binary',self.runvat_dir)
                break
            
        os.remove(self.runvat_dir+os.sep+self.inifile)
        shutil.copy(self.dump_binary_path+os.sep+'cfg_ini'+os.sep+self.inifile,
                    self.runvat_dir+os.sep+'Excalibur.ini')
        print(self.runvat_dir)
#######
#######
    def run_dump_phase(self):
        print('>>>> Enter run dump phase     >>>>')
        self.start_dump_batch()
        
    def start_dump_batch(self):
        self.batch = self.dump_binary_path+os.sep+'cfg_bat'+os.sep+self.batch

        with open(self.batch,'r') as bat:
            batlines = bat.readlines()
        if len(self.cmdidx_list) == 0:
            self.cmdidx_list = range(1,len(batlines)+1)
        print(self.cmdidx_list)
        for idx in self.cmdidx_list:
            print(idx)
            cmdline = batlines[idx - 1]
            cmdline = cmdline.replace('\n','')
            print('  >> '+cmdline)
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
                os.chdir(self.runvat_dir)
                os.system(cmd)
                print(key,name,cmd)
            except:
                pass
            finally:
                dump_result = self.result_path+os.sep+name
                if os.path.exists(dump_result):
                    os.rename(dump_result,self.result_path+os.sep+key+'_'+name)
    def kickoff_dumpenv(self):
        self.prepare_dump_phase()
        self.run_dump_phase()
        print('>>>> End   dump               >>>>')



if __name__ == '__main__':
    project = 'CHX001'
    binary  = '229881'
    batch   = 'H264_DEC_multislice.txt'
    inifile = 'Excalibur.ini'
    cmdidx_list = range(162,197)
    result_path = r'E:\hw\CHX001\dump'
    datmode  = 'BIN'
    usermodedrivername = 'igdumdim32.dll'

    dump_env_inst = dump_env(project,binary,batch,inifile,cmdidx_list,result_path,datmode,usermodedrivername)
    dump_env_inst.kickoff_dumpenv()
