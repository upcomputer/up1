# coding: utf-8
# 作者：程隆

import serial
import sys
import os
from PIL import Image
from datetime import datetime
import wx


class ImagecollectFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.baudrate = 115200

        # 串口号输入框
        self.portslist = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7',
                          'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14', 'COM15']
        self.portslabel = wx.StaticText(self, label=u"请选择串口号")
        self.portscombobox = wx.ComboBox(
            self, choices=self.portslist, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.choosePorts, self.portscombobox)

        # 滑块
        self.slider1 = wx.Slider(self, -1, 128, 0, 255,
                                 size=(300, 30), style=wx.SL_LABELS)  # 创建滑块控件
        self.slider1.SetTickFreq(5, 1)  # 滑块刻度间隔
        self.slider2 = wx.Slider(self, -1, 128, 0, 255,
                                 size=(300, 30), style=wx.SL_LABELS)  # 创建滑块控件
        self.slider2.SetTickFreq(5, 1)  # 滑块刻度间隔

        # 图像列数输入框
        self.clabel = wx.StaticText(self, label=u'列数')
        self.columnnumber = wx.TextCtrl(self)

        # 图像行数输入框
        self.llabel = wx.StaticText(self, label=u'行数')
        self.linenumber = wx.TextCtrl(self)

        # 确认按钮
        self.buttensure = wx.Button(self, label=u"确认并发送命令，获得图像")
        self.Bind(wx.EVT_BUTTON, self.onclicksure, self.buttensure)

        # 亮度输入框
        self.labeltip = wx.StaticText(self, label=u'调试部分：')
        self.lthres = wx.StaticText(self, label=u'亮度')

        # 对比度输入框
        self.ccontrast = wx.StaticText(self, label=u'对比度')

        # 对比度调整按钮
        self.butten_edit = wx.Button(self, label=u'更改图像')
        self.Bind(wx.EVT_BUTTON, self.onclick, self.butten_edit)

        # 历史状态状态栏显示栏

        # 布局
        self.rec_sizer = wx.FlexGridSizer(rows=3, cols=4, vgap=10, hgap=10)
        self.edit_sizer = wx.FlexGridSizer(rows=4, cols=2, vgap=10, hgap=10)
        self.box_sizer = wx.BoxSizer(orient=wx.VERTICAL)

        expand_option = dict(flag=wx.EXPAND)
        no_options = dict()
        empty_space = ((0, 0), no_options)

        for control, options in \
            [(self.portslabel, no_options),
             (self.portscombobox, no_options),
             empty_space,
             empty_space,
             (self.clabel, no_options),
             (self.columnnumber, no_options),
             (self.llabel, no_options),
             (self.linenumber, no_options),
             empty_space,
             (self.buttensure, no_options)]:
            self.rec_sizer.Add(control, **options)

        for control, options in \
            [(self.labeltip, no_options),
             empty_space,
             (self.lthres, no_options),
             (self.slider1, expand_option),
             (self.ccontrast, no_options),
             (self.slider2, expand_option),
             empty_space,
             (self.butten_edit, no_options)]:
            self.edit_sizer.Add(control, **options)

        for control, options in \
            [(self.rec_sizer, dict(border=20, flag=wx.ALL | wx.EXPAND)),
             (self.edit_sizer, dict(border=20, flag=wx.ALL | wx.EXPAND))]:
            self.box_sizer.Add(control, **options)

        self.SetSizerAndFit(self.box_sizer)

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
            if Line <= 240 and Line > 100:
                Linenumber = Line
                l = self.linenumber.Value
            elif Line <= 100 and Line > 0:
                Linenumber = Line
                l = '0' + self.linenumber.Value
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

    def onclick(self, event):
        try:
            thres = self.slider1.GetValue()
            if thres < 100 and thres > 0:
                thres = '0' + str(thres)
            elif thres < 255 and thres >= 100:
                thres = str(thres)
            else:
                raise Exception("Failure")
            print u"更改亮度为" + thres
            with serial.Serial(self.ports, self.baudrate, timeout=1) as ser:
                command = 't' + thres
                ser.write(command.encode(encoding="utf-8"))
                print command
        except serial.SerialException as e:
            print u'[错误]:不存在的串口，请使用 python -m serial.tools.list_ports 查看可用串口。\n将退出...'
            exit()
        except:
            print "[错误]:未选择串口！"
        try:
            contrast = self.slider2.GetValue()
            if contrast < 100 and contrast > 0:
                contrast = '0' + str(contrast)
            elif contrast < 255 and contrast >= 100:
                contrast = str(contrast)
            else:
                raise Exception("Failure")
            print u"更改对比度为" + contrast
            with serial.Serial(self.ports, self.baudrate, timeout=1) as ser:
                command = 'p' + contrast
                ser.write(command.encode(encoding="utf-8"))
                print command
        except serial.SerialException as e:
            print u'[错误]:不存在的串口，请使用 python -m serial.tools.list_ports 查看可用串口。\n将退出...'
            exit()
        except:
            print "[错误]:未选择串口！"
            exit()


app = wx.App(False)
frame = ImagecollectFrame(None, u"图像处理上位机")
frame.Show()
app.MainLoop()
