# -* - coding: UTF-8 -* -
'''

@author: zhaowei
'''
import os
from Common import const
from Common.userConf import UserConf

def scan_devices():
    "获取当前连接的设备"
    result = os.popen("adb devices").read()
    print result
    devices = result.split("\n")[1:]
    targets = []
    for device in devices:
        if device.strip():
            tmp = device.split()
            if len(tmp)==2 and tmp[1]=='device': 
                deviceInfo = {}
                deviceID = tmp[0]
                deviceInfo['id'] = deviceID
                deviceInfo["os"] = os.popen("adb -s %s shell getprop ro.build.version.release" % (deviceID)).read().strip()
                deviceInfo["name"] = os.popen("adb -s %s shell getprop ro.product.model" % (deviceID)).read().strip().replace(" ", "-")
                
                targets.append(deviceInfo)
    return targets

def getPackage():
    "获取apk的包名和Activity的名字"
    apkFile = ""
    apkPath = os.path.join(const.workSpace, "apk")
    commonPath = os.path.join(const.workSpace, "Common")
    aapthPath = os.path.join(commonPath, "aapt")
    for filename in os.listdir(apkPath):
        if filename.endswith(".apk"):
            apkFile = os.path.join(apkPath,filename)
            break
    commonStr = aapthPath+" dump badging "+apkFile
    print commonStr
    result = os.popen(commonStr).read()
    lines = result.split("\n")
    
    for line in lines:
        if line.startswith("package: name="):
            UserConf.packageName = line.split()[1].split("=")[1][1:-1]
            break
    for line in lines:
        if line.startswith("launchable-activity: name="):
            UserConf.activityName = line.split()[1].split("=")[1][1:-1]
            break
    
if __name__ == "__main__":
    getPackage()