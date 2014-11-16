# -*- coding: gbk -*- 
from distutils.core import setup
import py2exe
setup(console=['main.py'],data_files=[('',['config.ini','check.BAT','reset.BAT','Readme.txt'])])