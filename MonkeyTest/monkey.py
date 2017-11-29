#coding=utf-8


import os
from random import randint
import time


class Monkey(object):
    def __init__(self, logpath,device_id,pkgName):
        self.proName = "com.android.commands.monkey"
        
        self.logPath = logpath
        self.proportion = 100
        self.pkgName = pkgName
        self.device_id = device_id

        self.throttle = 500 #间隔时间，单位：毫秒
        self.runNum = 50000 #monkey动作次数
        
        '''动作选项说明
        --pct-touch：指定触摸事件的百分比，
        --pct-motion <percent> （滑动事件）、 
        --pct-trackball <percent> （轨迹球事件） 、 
        --pct-nav <percent> （导航事件 up/down/left/right）、 
        --pct-majornav <percent> (主要导航事件 back key 、 menu key)、 
        --pct-syskeys <percent> (系统按键事件 Home 、Back 、startCall 、 endCall 、 volumeControl)、 
        --pct-appswitch <percent> （activity之间的切换）、 
        --pct-anyevent <percent>（任意事件）
        '''
        #动作百分比配置，合计100%
        self.events = {"--pct-touch":35, "--pct-motion":15, "--pct-trackball":15,"--pct-nav":7,"--pct-majornav":8, 
                       "--pct-syskeys":10,"--pct-appswitch":5, "--pct-anyevent":5,"--pct-flip":0}
            
    
    def generateEventStr(self):
        "生成action字符串"
        eventStr = ""
        for key in self.events:
            eventStr = eventStr + " %s %s"%(key, self.events[key])
        return eventStr
    
    def generateCommand(self):
        "生成monkey命令行"
        seed = randint(100000000000, 200000000000)#随机事件种子值
        
        command = "adb -s %s shell monkey -p %s -s %d -v --throttle %s %s --ignore-crashes --ignore-timeouts\
         --ignore-security-exceptions --ignore-native-crashes --monitor-native-crashes "%(self.device_id,self.pkgName, seed, self.throttle, self.generateEventStr()) 
        
        command = command + str(self.runNum)
        return command
        
    @staticmethod
    def terminateMonkey(deviceID):
        def getMonekyPid():
            top = os.popen("adb -s %s shell top -n 1"%deviceID).read()
            for topItem in top.split("\n"):
                if "com.android.commands.monkey" in topItem:
                    return topItem.split()[0]
        pid = getMonekyPid()
        while pid:
            os.system("adb -s %s shell kill -9 %s"%(deviceID,pid))
            pid = getMonekyPid()
    
    def startMonkey(self):
        command = self.generateCommand()
        print(command)
        os.system("%s >> %s"%(command, os.path.join(self.logPath, "monkey.log")))
        