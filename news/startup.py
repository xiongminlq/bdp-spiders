# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: RunSpilders.py
@time: 2019/3/13 10:04
"""

import time
import schedule
import win32api
import win32gui
import win32con
import os
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import subprocess
import winreg


def openWeChat(name, position1, position2):
    handle = win32gui.FindWindow("WeChatMainWndForPC", '微信')
    # # 设置英文键盘
    # en = 0x4090409
    # win32api.LoadKeyboardLayout('0000' + hex(en)[-4:], 1)
    # win32api.SendMessage(
    #     handle,
    #     win32con.WM_INPUTLANGCHANGEREQUEST,
    #     0,
    #     en)
    # 窗口置顶
    win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, 0, 0, 710, 500, win32con.SWP_SHOWWINDOW)
    time.sleep(0.5)
    # # 定位到搜索框，点击输入搜索
    # win32api.SetCursorPos([150, 40])
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # time.sleep(0.5)
    # m = PyMouse()
    # k = PyKeyboard()
    # # 鼠标点击
    # m.click(150, 40, 1)
    # time.sleep(0.5)
    # # 键盘输入
    # k.type_string(name)
    # time.sleep(0.5)
    # # 鼠标单击事件
    # win32api.SetCursorPos([150, 125])
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # 点击聊天图标
    for i in range(3):
        win32api.SetCursorPos([30, 90])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.5)
    # 点击订阅号图标
    for i in range(3):
        win32api.SetCursorPos([150, 150])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.5)
    # 点击公众号
    for i in range(3):
        win32api.SetCursorPos(position1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.5)
    # 点击历史文章列表
    for i in range(3):
        win32api.SetCursorPos([685, 35])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.5)
        win32api.SetCursorPos(position2)
        # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(1)
    time.sleep(5)
    handle1 = win32gui.FindWindow("CefWebViewWnd", '微信')
    win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)
    win32gui.PostMessage(handle1, win32con.WM_CLOSE, 0, 0)


def start_spider():
    try:
        os.system("scrapy crawl bjwb")
        os.system("scrapy crawl bjrb")
        os.system("scrapy crawl cyb")
        os.system("scrapy crawl rmwly")
        os.system("scrapy crawl rmw")
        os.system("scrapy crawl tencent")
        os.system("scrapy crawl souhu")
        os.system("scrapy crawl sina")

        # 打开fiddler监控请求
        pid = subprocess.Popen('fiddler').pid
        time.sleep(5)
        # 打开微信，抓取东坝临友圈文章列表
        openWeChat('dongba100', [455, 100], [890, 190])
        os.system("scrapy crawl wechat")

        # 打开fiddler监控请求
        pid = subprocess.Popen('fiddler').pid
        time.sleep(5)
        # 打开微信，抓取东坝社区文章列表
        openWeChat('dongbacom', [455, 170], [890, 265])
        os.system("scrapy crawl wechat")
        # 关闭fiddler
        os.system('taskkill /pid ' + str(pid) + ' /f')

        # 清空代理设置，解决fiddler关闭后可能会没有清除代理设置的问题
        try:
            xpath = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, xpath, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, '')
            winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, '')
        except Exception as e:
            print("ERROR: " + str(e.args))
        print('生成词云')
        # os.system("python newswordcloud.py")
        now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        print('---{}---执行完成'.format(now_time))
        # 一定要先加载配置文件
    except Exception as e:
        print('--出现错误--', e)


if __name__ == '__main__':
    print('开始检测，等待时间到达，开始执行')
    schedule.every().day.at("00:00").do(start_spider)
    schedule.every().day.at("04:00").do(start_spider)
    schedule.every().day.at("08:00").do(start_spider)
    schedule.every().day.at("12:00").do(start_spider)
    schedule.every().day.at("16:00").do(start_spider)
    schedule.every().day.at("20:00").do(start_spider)
    # start_spider()

    while True:
        schedule.run_pending()
        time.sleep(10)
