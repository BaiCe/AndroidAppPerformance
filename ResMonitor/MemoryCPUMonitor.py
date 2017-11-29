#-*- coding: UTF-8 -*-

import threading
import os
import time
import subprocess
import sys
import signal
import re
from Common import const
from Common.userConf import UserConf

class memoryCPUMonitor(threading.Thread):
    over = False

    def __init__(self,logFolder,packageName,caseID=None,deviceID=None):
        threading.Thread.__init__(self)
        self.over = False
        self.package = packageName
        self.logFolder = logFolder
        
        if caseID is None:
            self.picPre = "Test"
            self.logFile = os.path.join(self.logFolder,"memory.log")
        else:
            self.picPre = caseID
            self.logFile = os.path.join(self.logFolder,"%s_memory.log"%caseID)
        if deviceID is None:
            self.cmdStr = 'adb shell "top -d 1 -s cpu | grep %s$" > "%s"'%(self.package,self.logFile )#间隔1秒获取一次
        else:
            self.cmdStr = 'adb -s %s shell "top -d 1 -s cpu | grep %s$" > "%s"'%(deviceID,self.package,self.logFile)
            
        self.over = False
        
    @staticmethod
    def terminate():
        memoryCPUMonitor.over = True
        
        
    def run(self):
        "开始执行"
        print "CPU/Memory监控启动...".decode("utf-8")
        print self.cmdStr
        sub_process = subprocess.Popen(self.cmdStr,shell=True)
        memoryCPUMonitor.over = False
        while not memoryCPUMonitor.over:
            time.sleep(1)
            
        else:
            time.sleep(10)
            print "数据收集结束。".decode("utf-8")
            os.system("taskkill /F /IM adb.exe")
        time.sleep(2)

        #处理文件路径中带空格的情况
        if " " in const.jarFile:
            cmdStr = 'java -jar "'+const.jarFile+'" "'+self.logFile+'" '+self.picPre+' "'+self.logFolder+'" 0 '+UserConf.packageName
        else:
            cmdStr = 'java -jar '+const.jarFile+' '+self.logFile+' '+self.picPre+' '+self.logFolder+' 0 '+UserConf.packageName
        if sys.platform.startswith("win"):
            subprocess.call(cmdStr)
        elif sys.platform.startswith('linux'):
            subprocess.call(cmdStr,shell=True)
        print "制图完毕。".decode("utf-8")
            

            
if __name__ == "__main__":

    print "over"