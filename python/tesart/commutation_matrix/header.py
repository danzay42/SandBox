# __________ external imports __________
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, \
    QRadioButton, QDialog, QGridLayout, QSizePolicy, QPushButton, QWidget
from PyQt5.QtCore import QThread, QSettings, QObject, pyqtSignal, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QColor, QPainter
import serial

# __________ internal imports __________
import time
import logging
import socket
import sys
import os
import subprocess
import ipaddress
import traceback
import netifaces

# __________ project files __________
from src.logger import logger
path = os.path.dirname(sys.argv[0])
matrix = 5
DEBUG = False
