#-*- coding: UTF-8 -*-
'''
Created on 2016-2-25

@author: zhaowei
'''
import os
import platform
import threading
import time
import sys
import subprocess
from Common import const
from Common.userConf import UserConf


class networkTraffic(threading.Thread):
    thread_stop = False
    total_bytes = 0
    def __init__(self,logFolder,deviceID,interval=1):
        threading.Thread.__init__(self)
        self.deviceNo = deviceID
        self.picPre = "Test"
        self.logFolder = logFolder
        self.pid = self.__getPid()
        self.uid = self.getAppUID()
        self.interval = interval
        bytesByUID = self.getBytesByUID()
        self.start_receive_bytes = bytesByUID[0]
        self.start_send_bytes = bytesByUID[1]
#         self.thread_stop = False
        self.logFile = logFolder+"/network.log"
        if os.path.exists(self.logFile):
            os.remove(self.logFile)
        self.networkLog = open(self.logFile,"a")
        self.networkLog.write("receiveBytes\tsendBytes\n")
        
    def run(self):
        print "流量监控启动...".decode("utf-8")
        networkTraffic.thread_stop = False
        time.sleep(3)
        while not networkTraffic.thread_stop:
            time.sleep(self.interval)
            bytesByUID = self.getBytesByUID()
            end_receive_bytes = bytesByUID[0]
            end_send_bytes = bytesByUID[1]
            receive_bytes = end_receive_bytes - self.start_receive_bytes
            send_bytes = end_send_bytes - self.start_send_bytes
            networkTraffic.total_bytes+= (receive_bytes+send_bytes)
            self.networkLog.write(str(receive_bytes)+"\t"+str(send_bytes)+"\n")
            self.start_receive_bytes = end_receive_bytes
            self.start_send_bytes = end_send_bytes
        else:
            self.networkLog.flush()
            self.networkLog.close()
        
        time.sleep(2)
        #处理文件路径中带空格的情况
        if " " in const.jarFile:
            cmdStr = 'java -jar "'+const.jarFile+'" "'+self.logFile+'" '+self.picPre+' "'+self.logFolder+'" 1 '+UserConf.packageName
        else:
            cmdStr = 'java -jar '+const.jarFile+' '+self.logFile+' '+self.picPre+' '+self.logFolder+' 1 '+UserConf.packageName
        if sys.platform.startswith("win"):
            subprocess.call(cmdStr)
        elif sys.platform.startswith('linux'):
            subprocess.call(cmdStr,shell=True)
        print "制图完毕。".decode("utf-8")
        
    @staticmethod        
    def terminate():
        networkTraffic.thread_stop = True
             
    def isWindowsSystem(self):
        return 'windows' in platform.system().lower()
     
    
    def __scanDevices(self):
        targets = []
        if self.isWindowsSystem():
            result = os.popen("adb devices").read()
            devices = result.split("\n")[1:]
                
            for device in devices:
                if device.strip():
                    tmp = device.split()
                    if len(tmp)==2 and tmp[1]=='device':
                        targets.append(tmp[0])
                
        return targets
    
    def getDeviceNo(self):
        devices = self.__scanDevices()
        if(len(devices)==0):
            raise Exception("手机没有连接，请连接手机")
        return devices[0]
    def getAppUID(self):
        "得到APP的UID"
        cmdStr = 'adb -s %s  shell "cat /proc/%s/status | grep Uid"' % (self.deviceNo,self.pid)
        uid = os.popen(cmdStr).read().split()[1]
        return uid
    
    def __getPid(self):
        "获取的PID，APP必须已经启动"
        try:
            cmdStr = 'adb -s %s shell "ps | grep %s$"' % (self.deviceNo,UserConf.packageName)
            pidStr = os.popen(cmdStr).read()
            pid = pidStr.split()[1]
            return pid
        except Exception as e:
            print "APP没有启动，启动APP...".decode("utf-8")
            self.app_start(UserConf.packageName,UserConf.activityName)
            time.sleep(5)
            return self.__getPid()

        
    def __getAppUIDByPackage(self):
        app_uid = os.popen('adb -s %s  shell su -c "cat /data/system/packages.list | grep %s"' % (self.deviceNo,UserConf.packageName)).read().split()[1]
        return app_uid
        
    def getReceiveBytes(self):
        "获取APP的接收的总字节数，手机重启后该数据会被清零，建议及时保存数据"
        cmdStr = "adb -s %s shell cat /proc/uid_stat/%s/tcp_rcv" % (self.deviceNo,self.uid)
        receiveBytes = os.popen(cmdStr).read().split("\n")[0]
        return long(receiveBytes)

    
    def getReceiveBytesByPid(self):
        "获取APP的接收的总字节数，手机重启后该数据会被清零，建议及时保存数据"
        self.pid = self.__getPid()
        cmdStr = 'adb -s %s shell "cat /proc/%s/net/dev |grep wlan0"' % (self.deviceNo,self.pid)
        receiveBytes = os.popen(cmdStr).read().split()[1]
        return long(receiveBytes)
    
    def getSendBytesByPid(self):
        "获取APP发送的总字节数，手机重启后该数据会被清零，建议及时保存数据"
        self.pid = self.__getPid()
        cmdStr = 'adb -s %s shell "cat /proc/%s/net/dev |grep wlan0"' % (self.deviceNo,self.pid)
        sendBytes = os.popen(cmdStr).read().split()[9]
        return long(sendBytes)
    
    def getBytesByUID(self):
        "获取APP的接收的总字节数，手机重启后该数据会被清零，建议及时保存数据"
        cmdStr = 'adb -s %s shell "cat /proc/net/xt_qtaguid/stats | grep %s | grep wlan0"' % (self.deviceNo,self.uid)
        rec_rows = os.popen(cmdStr).read().replace("\r","").split("\n")
        receiveBytes = 0
        sendBytes = 0
        for i in range(0,len(rec_rows)-1):
            row = rec_rows[i]
            receiveBytes+=long(row.split()[5])
            sendBytes+=long(row.split()[7])
        return [receiveBytes,sendBytes]
    
    def getSendBytes(self):
        "获取APP发送的总字节数，手机重启后该数据会被清零，建议及时保存数据"
        cmdStr = "adb -s %s shell cat /proc/uid_stat/%s/tcp_snd" % (self.deviceNo,self.uid)
        sendBytes = os.popen(cmdStr).read().split("\n")[0]
        return long(sendBytes)
    
    def app_start(self,packageName=UserConf.packageName,activityName=UserConf.activityName):
        "启动APP"
        cmdStr = "adb shell am start -n %s/%s"%(packageName,activityName)
        os.system(cmdStr)
        
if __name__ == "__main__":
    t = networkTraffic(r"C:\Users\zhaowei\Desktop\temp","9bae9a99")
    t.getBytesByUID()
