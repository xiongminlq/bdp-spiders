# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: test.py
@time: 2018/12/20 15:40
"""

import subprocess
import time
import os
import winreg

pid = subprocess.Popen('fiddler').pid
time.sleep(5)
print(pid)
os.system('taskkill /pid ' + str(pid) + ' /f')