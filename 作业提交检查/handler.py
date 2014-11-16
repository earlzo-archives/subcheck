# -*- coding: gbk -*- 
import os
from ConfigParser import ConfigParser
def banner():
	print '+--------------------------------------+'
	print '|          欢迎使用subcheck～          |'
	print '|       当前版本：V2.1.20141006        |'
	print '|     阅读Readme.txt了解更多说明       |'
	print '|                             By 二两丶|'
	print '+--------------------------------------+'
	
class Handler(ConfigParser):
	def __init__(self):
		self.firstuse=-1
		ConfigParser.__init__(self)
	#判断是否初次使用
	def first_use(self):
		self.set_path()
		self.firstuse=0
		self.set('Settings','first_use',self.firstuse)
		self.write(open('config.ini','wb+'))
		
	def start(self):
		#程序运行必须执行此函数
		try:
			self.read('config.ini')
		except IOError:
			print '配置文件打开失败，请确认程序目录下”config.ini“存在！'
			return 0
		self.firstuse=self.getint('Settings','first_use')
		
	def set_path(self):
		banner()
		path=raw_input('请输入本学期班级目录：').strip()
		while not os.path.exists(path) or os.path.isfile(path):
			print '设置失败！请确认您的目录是否正确～'
			path=raw_input('请输入本学期班级目录：').strip()
		else:
			self.set('Settings','path',path)
			print '设置成功～'
		#添加班级目录
		for content in os.listdir(path):
			contentpath=os.path.join(path,content)
			if not os.path.isfile(contentpath):
				try:
					self.add_section(content)
				except:
					pass
				self.set(content,'path',contentpath )
				print content,'已添加～'
		self.write(open('config.ini','wb+'))
		print os.linesep
		
	def reset(self):
		choice=raw_input('确定重置所有设置吗?[yes/no]').strip()
		while not choice=='yes' and not choice=='no':
			print '输入错误!请重新输入'
			choice=raw_input('确定重置所有设置吗?[yes/no]').strip()
		if choice=='yes':
			self.set('Settings','first_use','1')
			self.set('Settings','path','')
			sections=self.sections()
			sections.remove('Settings')
			for section in sections:
				self.remove_section(section)
				print section,'已从设置中清除'
			self.write(open("config.ini","wb+"))
		elif choice=='no':
			print '设置未做任何更改~'
if __name__=='__main__':
	print '请运行main.py开始程序！'
