#-*- coding: UTF-8 -*-
'''
Created on 2016-2-26

@author: zhaowei
'''
import os
from threading import Thread
import time
from Common.userConf import UserConf


class startTime(object):
    def __init__(self,times,packageName=UserConf.packageName,activityName=UserConf.activityName):
        self.packageName = packageName
        self.activityName = activityName  
        self.times = times

    def getStartTime(self):
        "获取App一次启动的时间（应用关闭已经关闭，不在后台）单位:毫秒"
        self.stopAPP()
        cmd = 'adb shell "am start -W -n  %s/%s | grep TotalTime"' % (self.packageName,self.activityName)
        time = os.popen(cmd).read().split(": ")[1]
        return long(time)
    
    def stopAPP(self):
        stopCmd = "adb shell am force-stop %s" % self.packageName
        os.system(stopCmd)
        
    def execute(self): 
        "根据给定的次数进行启动APP，获取APP的启动时间，以字典的形式返回，key分别为：max：最大时间，min最小时间，avg：平均时间，count：次数 ,单位:毫秒，默认次数为5次"
        r = []
        appStartTime = {}
        
        for i in xrange(self.times):
            startTime = self.getStartTime()
            r.append(startTime)
            print ("第"+str(i+1)+"次的启动时间为："+str(startTime)).decode("utf-8")
            time.sleep(1)
            
        appStartTime['max'] = max(r)
        appStartTime['min'] = min(r)
        appStartTime['avg'] = sum(r)/self.times
        if len(appStartTime)>2:
            r.sort()
            appStartTimeNotMaxAndNotMin = r[1:-1]
            appStartTime['avg'] = sum(appStartTimeNotMaxAndNotMin)/(self.times-2)
        appStartTime['count'] = self.times
        print appStartTime
        return appStartTime
     
          
            
if __name__ == "__main__":
    s = startTime(9)
    result = s.execute()
    print result