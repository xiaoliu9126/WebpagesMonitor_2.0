"""
coding:utf-8
file: common_util.py
@desc:
"""
import datetime
import hashlib

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMessageBox
import uuid
import frozen_dir
import yaml

SUPER_DIR = frozen_dir.app_path()

APP_ICON = SUPER_DIR + r'/res/img/main_logo.png'
SEARCH_ICON = SUPER_DIR + r'/res/img/main_search.png'
START_ICON = SUPER_DIR + r'/res/img/main_star.png'
WMR_ICON = SUPER_DIR + r'/res/img/main_WMR.png'

COURSE_FILE = SUPER_DIR + r'/data/coursefile.json'

USER_ALL_COURSE = SUPER_DIR

CONFIG_FILE_PATH = SUPER_DIR + r'/config/setting.yml'
PATTERS = ['^[0-9]{1,2}$']


def get_md5(data):
    """
    获取md5加密密文
    :param data: 明文
    :return: 加密后的密文
    """
    m = hashlib.md5()
    b = data.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()


def read_yaml(path):
    with open(path, encoding='utf-8') as f:
        stm = f.read()
    content = yaml.load(stm, Loader=yaml.FullLoader)
    return content

def msg_box(widget, title, msg):
    QMessageBox.warning(widget, title, msg, QMessageBox.Yes)

def accept_box(widget, title, msg):
    return QMessageBox.warning(widget, title, msg, QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

def get_current_time():
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt

def read_qss(qss_file):
    with open(qss_file, 'r', encoding='utf-8') as f:
        return f.read()

def get_return_day(day):
    return (datetime.datetime.now() + datetime.timedelta(days=day)).strftime('%Y-%m-%d %H:%M:%S')

def set_le_reg(widget, le, pattern):
    rx = QRegExp()
    rx.setPattern(pattern)
    qrx = QRegExpValidator(rx, widget)
    le.setValidator(qrx)

SYS_STYLE = read_qss(SUPER_DIR + r'/res/style.qss')

