# -* - coding: UTF-8 -* - 

import os,sys
import time


class Report(object):


    def __init__(self, results_dir):
        self.results_dir = results_dir
        timeStr = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.fn = os.path.join(results_dir,'result_%s.html'%timeStr)
        if not os.path.exists(self.fn):
            f = open(self.fn,'w')
            f.close()
        self.write_head_html()
        
    def write_line(self, line):
        with open(self.fn, 'a') as f:
            f.write('%s\n' % line)
        
    
    def write_head_html(self):
        with open(self.fn, 'w') as f:
            f.write("""\
                    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
                    <head>
                        <title>App性能测试报告(Android)</title>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                        <meta http-equiv="Content-Language" content="en" />
                        <style type="text/css">
                            h1 {
                                    font-size: 17pt;
                                    margin: 30px 0 5px 0;
                                }
                            p{
                              font-size:18px;
                              }
                                
                                .dataTable {
                                    border-collapse: collapse;
                                    border: 1px solid #000000;
                                    margin: 0;
                                }
                                
                                td {
                                    border: 1px solid #000000;
                                    margin: 0;
                                    padding-left: 5px;
                                    padding-right: 5px;
                                    vertical-align: top;
                                }
                                .td1{
                                border:none; 
                                margin:none; 
                                line-height:20px; 
                                padding:0px;
                                }
                                
                                .nameProduct{
                                    width: 1000px;
                                    word-break:break-all; 
                                    word-wrap:break-all;
                                }
                                
                                .nameNormal{
                                    width: 200px;
                                    word-break:break-all; 
                                    word-wrap:break-all;
                                }
                                
                                .resultFail{
                                    color:red;
                                }
                                
                                .resultNotRun{
                                    color:#D2691E;
                                }
                        </style>
                    </head>
                    <body>
                    """)
  

    def write_closing_html(self):
        with open(self.fn, 'a') as f:
            f.write("""\
                </body>
                </html>
                """)
