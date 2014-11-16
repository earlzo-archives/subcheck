# -*- coding: gbk -*- 
import os
from ConfigParser import ConfigParser
def banner():
	print '+--------------------------------------+'
	print '|          ��ӭʹ��subcheck��          |'
	print '|       ��ǰ�汾��V2.1.20141006        |'
	print '|     �Ķ�Readme.txt�˽����˵��       |'
	print '|                             By ����ؼ|'
	print '+--------------------------------------+'
	
class Handler(ConfigParser):
	def __init__(self):
		self.firstuse=-1
		ConfigParser.__init__(self)
	#�ж��Ƿ����ʹ��
	def first_use(self):
		self.set_path()
		self.firstuse=0
		self.set('Settings','first_use',self.firstuse)
		self.write(open('config.ini','wb+'))
		
	def start(self):
		#�������б���ִ�д˺���
		try:
			self.read('config.ini')
		except IOError:
			print '�����ļ���ʧ�ܣ���ȷ�ϳ���Ŀ¼�¡�config.ini�����ڣ�'
			return 0
		self.firstuse=self.getint('Settings','first_use')
		
	def set_path(self):
		banner()
		path=raw_input('�����뱾ѧ�ڰ༶Ŀ¼��').strip()
		while not os.path.exists(path) or os.path.isfile(path):
			print '����ʧ�ܣ���ȷ������Ŀ¼�Ƿ���ȷ��'
			path=raw_input('�����뱾ѧ�ڰ༶Ŀ¼��').strip()
		else:
			self.set('Settings','path',path)
			print '���óɹ���'
		#��Ӱ༶Ŀ¼
		for content in os.listdir(path):
			contentpath=os.path.join(path,content)
			if not os.path.isfile(contentpath):
				try:
					self.add_section(content)
				except:
					pass
				self.set(content,'path',contentpath )
				print content,'����ӡ�'
		self.write(open('config.ini','wb+'))
		print os.linesep
		
	def reset(self):
		choice=raw_input('ȷ����������������?[yes/no]').strip()
		while not choice=='yes' and not choice=='no':
			print '�������!����������'
			choice=raw_input('ȷ����������������?[yes/no]').strip()
		if choice=='yes':
			self.set('Settings','first_use','1')
			self.set('Settings','path','')
			sections=self.sections()
			sections.remove('Settings')
			for section in sections:
				self.remove_section(section)
				print section,'�Ѵ����������'
			self.write(open("config.ini","wb+"))
		elif choice=='no':
			print '����δ���κθ���~'
if __name__=='__main__':
	print '������main.py��ʼ����'
