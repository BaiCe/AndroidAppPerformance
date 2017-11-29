#coding=utf-8
'''

@author: zhaowei
'''
from threading import Thread
import os
import platform
import time
import datetime
import traceback
from monkey import Monkey
import utils

def getCurrentTime():
    return time.strftime("%m%d%H%M%S")

class MonkeyThread(Thread):
    def __init__(self, logPath,device_id, pkgName):
        Thread.__init__(self)
        
        self.monkeyInstance = Monkey(logPath,device_id,pkgName)
        self.logPath = logPath
        
     
    def run(self):
        self.monkeyInstance.startMonkey()
        
        
class monkeyTestProcess(object):
    
    def __init__(self, device_id, pkgName, log_path, minutes):
        self.pkgName = pkgName
        self.minutes = minutes
        
        self.crashCount = 0
        self.anrCount = 0
        
        self.crashInfo = []
        self.anrInfo = []
        
        self.tasksCrashCount = 0
        self.tasksAnrCount = 0
        
        print("StabilityTask-log_path is %s"%(log_path))
        self.logPath = log_path
        self.monkeyLogPath = os.path.join(self.logPath, "monkey.log")
        
        self.deviceId = device_id
        self.tasks = {}
        self.tasks["pkgName"] = self.pkgName
        self.tasks["duration"] = self.minutes
        self.tasks["deviceID"] = device_id
    
    
    def crash_analyse(self,crashCount): 
            
        f = open(self.monkeyLogPath,'r')   # 返回一个文件对象
        line = f.readline()                # 调用文件的 readline()方法 
        flag = 1
        for i in range(0, int(crashCount)):
            result = '' 
            while line:
                if flag == 1:
                    if not line.find('CRASH') == -1:
                        result += line
                        flag = 0
                else:
                    if not line.find('//') == -1:
                        if not line.find('CRASH') == -1:
                            flag = 1
                            break
                        else:
                            result += line
                    else:
                        flag = 1
                        break
                line = f.readline()
                
            self.crashInfo.append(result)
            
        f.close()
        
        
    def anr_analyse(self,anrCount): 
        f = open(self.monkeyLogPath,'r')  # 返回一个文件对象
        line = f.readline()               # 调用文件的 readline()方法 
        flag = 1
        for i in range(0, int(anrCount)):
            result = '' 
            while line:
                if flag == 1:
                    if not line.find('NOT RESPONDING') == -1:
                        result += line
                        flag = 0
                else:
                    if not line.find('anr traces status was 0') == -1:
                        flag = 1
                        break
                    else:
                        result += line
                line = f.readline()
                
            self.anrInfo.append(result)
            
        f.close()
    
    
    def analyse(self):
        
        if platform.system() == "Windows":
            crashCount = os.popen('type %s|find "CRASH:" /c'%(self.monkeyLogPath,)).read().strip()
            anrCount = os.popen('type %s|find "ANR " /c'%(self.monkeyLogPath,)).read().strip()
        else:
            crashCount = os.popen('grep -c "CRASH:" %s'%(self.monkeyLogPath,)).read().strip()
            anrCount = os.popen('grep -c "ANR " %s'%(self.monkeyLogPath,)).read().strip()
        
        self.crash_analyse(crashCount)
        self.anr_analyse(anrCount)
        
        self.tasksCrashCount = int(crashCount)
        self.tasksAnrCount = int(anrCount)
    
    def collect(self):
        utils.getLog(self.logPath,self.deviceId)
        utils.getTraceData(self.logPath,self.deviceId)
        
    def execute(self):
        
        startTime = time.time()
        print("monkey开始时间：%s"%(datetime.datetime.now())).decode("utf-8")
        monkeyThreadInstance = MonkeyThread(self.logPath,self.deviceId,self.pkgName)
        utils.forceStop(self.pkgName,self.deviceId)
        if not os.path.exists(self.logPath):
            os.makedirs(self.logPath)
        
        try:
            monkeyThreadInstance.start()
            
            while True:
                endTime = time.time()
                # 清除之前的日志
#                 utils.clearLog(self.deviceId)
                
                if (endTime-startTime) < self.minutes*60:
                    if monkeyThreadInstance.is_alive():
                        time.sleep(10)
                    else:
                        utils.forceStop(self.pkgName,self.deviceId)
                        if not os.path.exists(self.logPath):
                            os.makedirs(self.logPath)

                        monkeyThreadInstance = MonkeyThread(self.deviceId,self.pkgName)
                        monkeyThreadInstance.start()
                else:
                    print("monkey结束时间：%s"%(datetime.datetime.now())).decode("utf-8")
                    Monkey.terminateMonkey(self.deviceId)
                    
                    self.collect()
                    self.analyse()
                    break
        except Exception,e:
            print("Monkey Exception:"%(e))
            print("Monkey traceback:"%(traceback.print_exc()))
            traceback.print_exc()
            Monkey.terminateMonkey(self.deviceId)
            self.collect()
            self.analyse()
            
        finally:
            
            self.tasks['crashCount'] = str(self.tasksCrashCount)
            if self.tasksCrashCount != 0:
                self.tasks['crashInfo'] = self.crashInfo
            
            self.tasks["anrCount"] = str(self.tasksAnrCount)
            
            if self.tasksAnrCount != 0:
                self.tasks['anrInfo'] = self.anrInfo

            print self.tasks
            return self.tasks

if __name__ == "__main__":
    result = monkeyTestProcess("", "", r'd:/test/logs', 1).start()
