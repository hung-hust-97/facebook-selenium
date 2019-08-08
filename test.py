#!/usr/bin/env python

# pymotm.py


# # Method add_argument()
#
# import argparse
#
# parser = argparse.ArgumentParser(description="Example for store true & false")
# parser.add_argument('--set-false', '--s', '--sf', help= "Set var_name to false", dest= 'var_name', action='version', version='%(prog)s 1.0')
# parser.set_defaults(var_name =True)
# args = parser.parse_args()
# print("var_name is %s " % args.var_name)

# Đoạn này để đảm bảo rằng khi chương trình được chạy mà không truyền tham số gì thì nó sẽ hiển thị phần trợ giúp chi
# tiết. Nếu bạn copy đoạn code này để thử. Vui lòng xóa đoạn comment này trước khi chạy chương trình.
# if __name__ == "__main__":
#     parser.print_help()

#
# # Action classes
#
# import argparse
# import getpass
#
# class Password(argparse.Action):
#     def __call__(self, parser, namespace, values, option_string):
#         if values is None:
#             values = getpass.getpass(prompt="Enter MySQL password: ")
#
#         setattr(namespace, self.dest, values)
#
# parser = argparse.ArgumentParser(description="Simple MySQL command-line :))")
# parser.add_argument("-u", dest="username", help="Enter MySQL username")
# parser.add_argument("-p", dest="password", help="Enter password for MySQL username", action=Password, nargs="?")
#
# args = parser.parse_args()
#
# print ("Username: %s\nPassword: %s" % (args.username, args.password))


# Method parse_args()


# cookies

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import sys, os, re, json
from datetime import datetime
import pickle
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import numpy as np
import time
import argparse   #Command line option and argument parsing (phân tích các tham số và tùy chọn trên ... )



# Mở file trong chế độ ghi trong định dạng nhị phân.
# with open('cookies.pkl', 'rb') as cookiesfile:
#     cookies = pickle.load(cookiesfile)  # unpickling tạo lại đối tượng cookies từ chuỗi cookiesfile
#     for cookie in cookies:
#         print(cookie)



#
#
# ts = time.time()
# print(ts)

#
# line = "Hoc Python la defdsf sdfsdf hon hoc Java?"
#
# matchObj = re.match( r'thon', line, re.M|re.I)
# if matchObj:
#    print ("match --> matchObj.group() : ", matchObj.group())
# else:
#    print ("Khong co ket noi!!")
#
# searchObj = re.search( r'thon', line, re.M|re.I)
# if searchObj:
#    print ("search --> searchObj.group() : ", searchObj.group())
# else:
#    print ("Khong tim thay!!")

import re

line = "Hoc Python la defdsf sdfsdf hon hoc Java?"

matchObj = re.match( r'(.*) la (.*) hon (.*?) ', line, re.M|re.I)

if matchObj:
   print ("matchObj.group() : ", matchObj.group())
   print ("matchObj.group(1) : ", matchObj.group(1))
   print ("matchObj.group(2) : ", matchObj.group(2))
   print("matchObj.group(2) : ", matchObj.group(3))
else:
   print ("Khong co ket noi!!")