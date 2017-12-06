# -* - coding: UTF-8 -* -

import time

from Tkinter import *
import os
import tkMessageBox
from ResMonitor.MemoryCPUMonitor import memoryCPUMonitor
from ResMonitor.NetworkTraffic import networkTraffic
from ResMonitor.PowerMonitor import powerMonitor
from Common import util, const
from MonkeyTest.MonkeyTestProcess import monkeyTestProcess
from StartTime.StartTime import startTime
import threading
import traceback
from Report.generateReport import generateReportEx
from Common.userConf import UserConf

class mainWindow(object):
    def __init__(self):
        self.root = Tk()
        self.cpuMonitor = None
        self.networkMonitor = None
        self.powerMonitor = None
        self.monkeyCheckVar = IntVar()
        self.startTimeCheckVar = IntVar()
        self.cpuCheckVar = IntVar()
        self.networkCheckVar = IntVar()
        self.powerCheckVar = IntVar()
        
        #设置窗口属性
        self.__initWindow()
        #初始化测试选项区域
        self.__initTestItem()
        #初始化资源监控选项区域
        self.__initResMonitor()
        #初始化窗口底部功能按钮区域
        self.__initButtonFrame()
        
        self.root.mainloop()
        
        
    def __initWindow(self):
        "初始化窗口设置，标题、大小、icon等"
        
        self.root.title("Android性能测试工具_BestTest")
        
        self.root.minsize(480, 350)
        #设置窗口在屏幕中央显示
        scnWidth,scnHeight = self.root.maxsize() 
        tmpcnf = "480x350+%d+%d"%((scnWidth/2-240),(scnHeight/2-175))
        self.root.wm_geometry(tmpcnf)
        
        self.root.iconbitmap(os.path.join(const.resPath,"logo.ico"))
        self.root.resizable(width=False, height=False)
#         self.root.设置背景图片
        
        
    def __initTestItem(self):
        "初始化测试项frame"
        self.frame_testItem = LabelFrame(self.root,text="测试项选择",width=430,height=90,font=('Arial', 15))#,padx=50,pady=30
        self.frame_testItem.grid(row=0,column=0,padx=20,pady=10,ipadx=3,ipady=3)
        self.frame_testItem.grid_propagate(0) # 使组件大小不变，此时width才起作用
        
        self.chb_monkey = Checkbutton(self.frame_testItem,text="monkey测试",font=('Arial', 12),variable = self.monkeyCheckVar, \
                onvalue = 1, offvalue = 0,command = self.__monkeySetting)
        lb_time = Label(self.frame_testItem,text="执行时长：",font=('Arial', 12))
        self.tb_time = Entry(self.frame_testItem,state=DISABLED)
        lb_minutes = Label(self.frame_testItem,text="分钟",font=('Arial', 12))
        
        self.chb_startTime = Checkbutton(self.frame_testItem,text="启动时间测试",font=('Arial', 12),variable = self.startTimeCheckVar, \
                 onvalue = 1, offvalue = 0,command = self.__startTiemsSetting)
        lb_times = Label(self.frame_testItem,text="执行次数：",font=('Arial', 12))
        self.tb_times = Entry(self.frame_testItem,state=DISABLED)
        lb_t = Label(self.frame_testItem,text="次",font=('Arial', 12))
        
        
        self.chb_monkey.grid(row=0, column=0,sticky=W)
        lb_time.grid(row=0, column=1)
        self.tb_time.grid(row=0, column=2)
        lb_minutes.grid(row=0, column=3)
        
        self.chb_startTime.grid(row=1, column=0,sticky=W)
        lb_times.grid(row=1, column=1)
        self.tb_times.grid(row=1, column=2)
        lb_t.grid(row=1, column=3)
        
        
    
        
    def __initResMonitor(self):
        "初始化资源监控frame"
        self.fram_resmonitor = LabelFrame(self.root,text="资源监控设置",width=430,height=120,font=('Arial', 15))#,padx=50,pady=30
        self.fram_resmonitor.grid(row=1,column=0,sticky=W,padx=20,pady=10,ipadx=3,ipady=3)
        self.fram_resmonitor.grid_propagate(0)#保障frame的尺寸设置生效
        
        self.chb_cpu = Checkbutton(self.fram_resmonitor,text="cpu、内存资源",font=('Arial', 12),variable = self.cpuCheckVar, \
                 onvalue = 1, offvalue = 0)
        self.chb_network = Checkbutton(self.fram_resmonitor,text="流量监控",font=('Arial', 12),variable = self.networkCheckVar, \
                 onvalue = 1, offvalue = 0)
        self.chb_power = Checkbutton(self.fram_resmonitor,text="电量监控",font=('Arial', 12),variable = self.powerCheckVar, \
                 onvalue = 1, offvalue = 0,state=DISABLED)
        
        self.chb_cpu.grid(row=0,column=0,sticky=W)
        self.chb_network.grid(row=1,column=0,sticky=W)
        self.chb_power.grid(row=2,column=0,sticky=W)
        
    def __initButtonFrame(self):
        "初始化底部功能按钮frame"
        self.frame_btns = Frame(self.root)
        self.frame_btns.grid(row=2,column=0,pady=40)
        
        self.btn_scanDevices = Button(self.frame_btns,text="设备检测",width=8,font=('Arial', 12),command = self.scanDevices)
        self.btn_start = Button(self.frame_btns,text="开始",width=8,font=('Arial', 12),command = self.start)
        self.btn_end = Button(self.frame_btns,text="结束",width=8,font=('Arial', 12),command = self.terminate)#,state=DISABLED
        self.btn_quit = Button(self.frame_btns,text="退出",width=8,bg = 'red',font=('Arial', 12),command = self.quit)
        
        self.btn_scanDevices.grid(row=0,column=0)
        self.btn_start.grid(row=0,column=1)
        self.btn_end.grid(row=0,column=2)
        self.btn_quit.grid(row=0,column=3)
        
    def __monkeySetting(self):
        "实现时长输入框的禁用与启用"
        if self.monkeyCheckVar.get() == 1:
            self.tb_time['state'] = NORMAL
            self.tb_time.focus()
        else:
            self.tb_time['state'] = DISABLED
        
    def __startTiemsSetting(self):
        "实现次数输入框的禁用与启用"
        if self.startTimeCheckVar.get() == 1:
            self.tb_times['state'] = NORMAL
            self.tb_times.focus_set()
        else:
            self.tb_times['state'] = DISABLED
        
    def quit(self):
        "关闭窗口，退出程序"
        self.root.quit()
    
    def scanDevices(self):
        "扫描手机设备"
        devices = util.scan_devices()
        if len(devices)>0:
            msg = "当前连接设备："
            for d in devices:
                msg += "%s%s"%(os.linesep,str(d).replace("'", ""))
            tkMessageBox.showinfo("提示", msg)
        else:
            tkMessageBox.showwarning("警示", "未连接手机设备，请检查！")
        
            
    def start(self):
        "开始执行测试"
        self.resultDict = {}
        #设备检测
        devices = util.scan_devices()
        
        if len(devices)<=0:
            tkMessageBox.showwarning("警示", "未连接手机设备，请检查！")
            return
        deviceID= devices[0]['id']
        #获取包名
        util.getPackage()
        if UserConf.packageName=="":
            tkMessageBox.showwarning("警示", "包名获取失败，请将apk文件放到工程目录下的apk目录下，文件以.apk结尾")
            return
        if UserConf.activityName=="":
            tkMessageBox.showwarning("警示","ActivityName获取失败，请将apk文件放到工程目录下的apk目录下，文件以.apk结尾")
            return
        print "PackageName: "+UserConf.packageName
        print "ActivityName: "+UserConf.activityName
        #资源勾选检测
        if self.cpuCheckVar.get() == 0 and self.networkCheckVar.get()==0 and self.powerCheckVar.get() == 0:
            tkMessageBox.showwarning("警示", "未选中任何资源监控，请至少选择一项！")
            return
        #monkey测试检查
        if self.monkeyCheckVar.get() == 1 and self.tb_time.get() == "":
            tkMessageBox.showerror("提示", "请输入monkey执行时间！")
            return
        #启动时间测试检查
        if self.startTimeCheckVar.get() == 1 and self.tb_times.get() == "":
            tkMessageBox.showerror("提示", "请输入启动时间得测试次数！")
            return
        
        if self.monkeyCheckVar.get() == 0 and self.startTimeCheckVar.get()==0:
            tkMessageBox.showinfo("提示", "未选中任何测试项，所以，您必须亲自在手机上点点点了~")
        self.resultDict["startTime"] = time.strftime("%Y/%m/%d %H:%M:%S")
        
        #创建文件夹
        self.resultFolder = os.path.join(const.logPath,"task_%s"%time.strftime("%m%d%H%M%S"))
        if not os.path.exists(self.resultFolder):
            os.mkdir(self.resultFolder)
        
        
        #开启资源监控器
        if self.cpuCheckVar.get() == 1:
            self.cpuMonitor = memoryCPUMonitor(logFolder=self.resultFolder,packageName=UserConf.packageName)
            self.cpuMonitor.start()
            
        if self.networkCheckVar.get() == 1:
            self.networkMonitor = networkTraffic(self.resultFolder,deviceID)
            self.networkMonitor.start()
            
        if self.powerCheckVar.get() == 1:
            self.powerMonitor = powerMonitor(logFolder=self.resultFolder)
            self.powerMonitor.start()
        
        if self.monkeyCheckVar.get() == 1 or self.startTimeCheckVar.get() == 1:
            try:  
                itemList = []
                monkeyTime = 0
                times = 0
                
                if self.monkeyCheckVar.get() == 1:
                    itemList.append("monkeytest")
                    monkeyTime = int(self.tb_time.get())
                if self.startTimeCheckVar.get() == 1:
                    itemList.append("starttimetest")
                    times = int(self.tb_times.get())
                    
                taskT = taskThread(itemList,self.resultFolder,deviceID,times,monkeyTime)
                taskT.start()
            except Exception:
                print traceback.format_exc()
        else:
            print "手动执行".decode("utf-8")
        
    def terminate(self):
        "停止测试"
        tkMessageBox.showwarning("警示", "您已停止测试，请稍后查看结果！")
        self.btn_start['state'] = ACTIVE
        
        powerMonitor.terminate()
        memoryCPUMonitor.terminate()
        networkTraffic.terminate()
        time.sleep(30)#需要等待制图结束
        self.resultDict["endTime"] = time.strftime("%Y/%m/%d %H:%M:%S")
        stime = time.mktime(time.strptime(self.resultDict["startTime"],'%Y/%m/%d %H:%M:%S'))
        etime = time.mktime(time.strptime(self.resultDict["endTime"],'%Y/%m/%d %H:%M:%S'))
        utime = etime - stime
        self.resultDict["useTime"] = str(utime)
        self.resultDict["testItems"] = {}
        generateReportEx(self.resultDict,self.resultFolder)
#         tkMessageBox.showinfo("提示", "报告已生成。请到文件夹%s下查看。"%self.resultFolder)
        
        
class taskThread(threading.Thread):
    def __init__(self,itemList,path,deviceID,startTimes=0,monkeyTime=0):
        threading.Thread.__init__(self)
        self.itemList = itemList
        self.path = path
        self.deviceID = deviceID
        self.startTimes = startTimes
        self.monkeyTime = monkeyTime
        
        
    def run(self):
        resultDict = {}
        resultDict["startTime"] = time.strftime("%Y/%m/%d %H:%M:%S")
        tmp = {}
        try:
            for item in self.itemList:
                if item == "monkeytest":
                    "执行monkey测试"
                    monkeyTest = monkeyTestProcess(self.deviceID,UserConf.packageName,self.path,self.monkeyTime)
                    r1 = monkeyTest.execute()
                    tmp["monkeyTest"] = r1
                if item == "starttimetest":
                    "执行启动时间测试"
                    self.startTest = startTime(self.startTimes,UserConf.packageName,UserConf.activityName)
                    r2 = self.startTest.execute()
                    tmp["startTime"] = r2
        except Exception:
            print traceback.format_exc()
        finally:
            powerMonitor.terminate()
            memoryCPUMonitor.terminate()
            networkTraffic.terminate()
            resultDict["testItems"] = tmp
            resultDict["endTime"] = time.strftime("%Y/%m/%d %H:%M:%S")
            stime = time.mktime(time.strptime(resultDict["startTime"],'%Y/%m/%d %H:%M:%S'))
            etime = time.mktime(time.strptime(resultDict["endTime"],'%Y/%m/%d %H:%M:%S'))
            utime = etime - stime
            resultDict["useTime"] = str(utime)
            time.sleep(30)#需要等待制图结束
            generateReportEx(resultDict,self.path)
        
        
if __name__ == "__main__":
    m = mainWindow()