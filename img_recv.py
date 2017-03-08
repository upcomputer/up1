# coding: utf-8

import serial
import sys
import os
from PIL import Image
from datetime import datetime

if len(sys.argv) < 4:
    print('[用法]: {} <port> <ccc> <rrr>'.format(sys.argv[0]))
    exit()

try:
    nc = int(sys.argv[2], 10)               # 列数
    nr = int(sys.argv[3], 10)               # 行数

    baudrate = 115200
    timeout = int((nc * nr / (baudrate / 8) + 5) * 2)
    with serial.Serial(sys.argv[1], baudrate, timeout=timeout) as ser:
        print(
            '[信息]:准备接收图像，按任意键继续...')
        os.system('pause')
        command = 'i' + sys.argv[2] + sys.argv[3]
        ser.write(command.encode(encoding="utf-8"))
        print(command)
        imgbuff = ser.read(nc * nr)
        print('RECEVIED {} BYTES'.format(len(imgbuff)))
        i = Image.frombytes(mode='L', size=(nc, nr), data=imgbuff)
        dt = datetime.now()
        i.save('DBG' + dt.strftime('%y%m%d%H%M%S') + '.jpg')
except serial.SerialException as e:
    print(
        '[错误]:不存在的串口{}，请使用 python -m serial.tools.list_ports 查看可用串口。\n将退出...'
        .format(sys.argv[1]))
    exit()
