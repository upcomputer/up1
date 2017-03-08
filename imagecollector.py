# coding: utf-8

import serial
import sys
import os
from PIL import Image
from datetime import datetime
import wx


class ImagecollectPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(800, 800))
        self.baudrate = 115200

        # 串口号输入框
        self.portslist = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7',
                          'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14', 'COM15']
        self.portslabel = wx.StaticText(self, label=u"请选择串口号")
        self.portscombobox = wx.ComboBox(self, size=(
            90, -1), choices=self.portslist, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.choosePorts, self.portscombobox)

        # 滑块
        slider = wx.Slider(self, -1, 30, 1, 100,
                           size=(250, -1))  # 创建滑块控件
        slider.SetTickFreq(5, 1)  # 滑块刻度间隔

        # 图像列数输入框
        self.clabel = wx.StaticText(self, label=u'列数')
        self.columnnumber = wx.TextCtrl(self)

        # 图像行数输入框
        self.llabel = wx.StaticText(self, label=u'行数')
        self.linenumber = wx.TextCtrl(self, size=(40, -1))

        # 确认按钮
        self.buttensure = wx.Button(self, label=u"确认并发送命令，获得图像")
        self.Bind(wx.EVT_BUTTON, self.onclicksure, self.buttensure)

        # 亮度输入框
        self.labeltip1 = wx.StaticText(self, label=u'调试部分1：')
        self.lthres = wx.StaticText(self, label=u'亮度')
        self.thres = wx.TextCtrl(self)

        # 亮度调整按钮
        self.buttenthres = wx.Button(self, label=u"更改图像亮度")
        self.Bind(wx.EVT_BUTTON, self.onclickthres, self.buttenthres)

        # 对比度输入框
        self.labeltip2 = wx.StaticText(self, label=u'调试部分2：')
        self.ccontrast = wx.StaticText(self, label=u'对比度')
        self.contrast = wx.TextCtrl(self, size=(40, -1))

        # 对比度调整按钮
        self.buttencontrast = wx.Button(self, label=u'更改图像对比度')
        self.Bind(wx.EVT_BUTTON, self.onclickcontrast, self.buttencontrast)

        # 历史状态状态栏显示栏

        # 布局
        self.rec_sizer = wx.FlexGridSizer(rows=3, cols=4, vgap=10, hgap=10)
        self.edit_sizer = wx.FlexGridSizer(row=4, clos=2, vgap=10, hgap=10)

        expand_option = dict(flag=wx.EXPAND)
        no_options = dict()

    # 选择串口方法
    def choosePorts(self, event):
        print u"选择串口号" + self.portscombobox.Value
        self.ports = self.portscombobox.Value

    # 确认并发送命令方法
    def onclicksure(self, event):
        Columnnumber = 240
        Linenumber = 80
        c = '240'
        l = '080'
        try:
            Column = int(self.columnnumber.Value)
            Line = int(self.linenumber.Value)
            if Column <= 240 and Column > 0:
                Columnnumber = Column
                c = self.columnnumber.Value
            else:
                print "行数格式错误，默认输入行数 %d" % Columnnumber
            if Line <= 240 and Line > 0:
                Linenumber = Line
                l = self.linenumber.Value
            else:
                print "列数输入错误，默认输入列数 %d" % Linenumber
        except:
            print "行数列数格式错误，默认输入行数 %d 列数 %d" % (Columnnumber, Linenumber)
        try:
            timeout = int((Columnnumber * Linenumber /
                           (self.baudrate / 8) + 5) * 2)
            with serial.Serial(self.ports, self.baudrate, timeout=timeout) as ser:
                print u'[信息]：准备接受图像，按任意键继续'
                os.system('pause')
                command = 'i' + c + l
                ser.write(command.encode(encoding="uft-8"))
                print u'已输入:' + command
                imgbuff = ser.read(Columnnumber * Linenumber)
                print u'已接受%d Bytes' % imgbuff
                i = Image.frombytes(mode='L', size=(
                    Columnnumber, Linenumber), data=imgbuff)
                dt = datetime.now()
                i.save('DBG' + dt.strftime('%y%d%H%M%S') + 'jpg')
        except:
            print u'[错误]:不存在的串口，请使用 python -m serial.tools.list_ports 查看可用串口。\n将退出...'
            exit()

    def onclickthres(self, event):
        try:
            thres = self.thres.Value
            print u"更改亮度为" + thres
            with serial.Serial(self.ports, self.baudrate, timeout=1) as ser:
                command = 't' + thres
                ser.write(command.encode(encoding="utf-8"))
                print command
        except serial.SerialException as e:
            print u'[错误]:不存在的串口，请使用 python -m serial.tools.list_ports 查看可用串口。\n将退出...'
            exit()
        except:
            print "未输入更改亮度的值，或不在范围内(0-256)默认128，将退出"
            exit()

    def onclickcontrast(self, event):
        try:
            contrast = self.contrast.Value
            print u"更改对比度为" + contrast
            with serial.Serial(self.ports, self.baudrate, timeout=1) as ser:
                command = 'p' + contrast
                ser.write(command.encode(encoding="utf-8"))
                print command
        except serial.SerialException as e:
            print u'[错误]:不存在的串口，请使用 python -m serial.tools.list_ports 查看可用串口。\n将退出...'
            exit()
        except:
            print "未输入更改对比度的值，或不在范围内(0-256)默认128，将退出"
            exit()


app = wx.App(False)
frame = wx.Frame(None)
panel = ImagecollectPanel(frame)
frame.Show()
app.MainLoop()
