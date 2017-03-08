# coding: utf-8
import sys
import serial

if len(sys.argv) < 3:
    print('[用法]: {} <port> <ttt>'.format(sys.argv[0]))
    exit()

try:

    baudrate = 115200
    timeout = 1
    with serial.Serial(sys.argv[1], baudrate, timeout=timeout) as ser:
        command = 't' + sys.argv[2]
        ser.write(command.encode(encoding="utf-8"))
        print(command)
except serial.SerialException as e:
    print(
        '[错误]:不存在的串口{}，请使用 python -m serial.tools.list_ports 查看可用串口。\n将退出...'
        .format(sys.argv[1]))
    exit()
