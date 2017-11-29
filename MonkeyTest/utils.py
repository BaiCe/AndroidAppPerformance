#coding=utf-8

import os
import zipfile

    
def clearLog(deviceID):
    os.system("adb -s %s shell logcat -c"%deviceID)
    
def getLog(logPath,deviceID):
    logcatPath = os.path.join(logPath, "logcat.log")
    os.system("adb -s %s shell logcat -d > %s"%(deviceID,logcatPath))
    
def dumpState(logPath,deviceID):
    dumpStateLogPath = os.path.join(logPath, "dumpState.log")
    os.system("adb -s %s shell dumpstate > %s"%(deviceID,dumpStateLogPath))

def getTraceData(logPath,deviceID):
    os.system("adb -s %s pull /data/anr %s"%(deviceID,logPath))
   
#可能获取到多个设备 
def getDeviceInfo():
    return os.popen("adb shell getprop ro.build.fingerprint").read().strip()
    
def compressFolder(folderPath):

    f = zipfile.ZipFile('abc.zip', 'w')
    for item in os.listdir(folderPath):
        f.write(os.path.join(folderPath, item))
    f.close()

def forceStop(packageName,deviceID):
    os.system("adb -s %s shell am force-stop %s"%(deviceID,packageName))
    cmd1 = 'adb -s %s shell ps | grep %s'%(deviceID,packageName)
    cmd2 = 'adb -s %s shell ps | find %s'%(deviceID,packageName)
    result = os.popen(cmd1).read()
    if result is None or result == "":
        result = os.popen(cmd2).read()
    if result is not None and result != "":
        lines = result.split("\n")
        for i in xrange(len(lines)):
            infos = lines[i].split()
            if infos[8]==packageName:
                pid = infos[1]
                break
        os.system('adb -s %s shell su -c "kill -9 %s"'%(deviceID,pid))

def reboot(deviceID=None):
    if deviceID is None:
        os.system("adb reboot")
    else:
        os.system("adb -s %s reboot"%deviceID)
    
