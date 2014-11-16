# -*- coding: gbk -*- 
import os,re,ConfigParser
from sys import exit
#Test,StudentΪԤ����
class Test:
	def __init__(self, name, path):
		self.name=name
		self.path=path
		self.notsub=[]
class Student:
	def __init__(self,idnum,name):
		self.idnum=idnum
		self.name=name
		self.pat=re.compile(r'([0-9]{10})')
class Classes:
	#�෽������������ϵ��ִ��˳������
	def __init__(self,classname, classpath):
		self.classname=classname
		self.classpath=classpath
		self.tests={}
		self.namelistpath=os.path.join(self.classpath,'NameList.txt')
		self.stus=[]
		self.stunum=0
		self.pat=re.compile(r'([0-9]{10})')
		self.statisticspath=os.path.join(self.classpath,'Statistics.txt')
		self.statistics=ConfigParser.ConfigParser()

	def add_test(self):
		#�����ڴ�������˿���Ŀ¼
		self.statistics.read(self.statisticspath)
		contents=os.listdir(self.classpath)
		for content in contents:
			testpath=os.path.join(self.classpath,content)
			if not os.path.isfile(testpath):
				if not self.statistics.has_section(content):
					self.statistics.add_section(content)
					print '�������',self.classname,content,'��Ŀ¼'
				else:
					print self.classname,content,'�Ѵ���'
				#�����еĿ��������ڴ�
				self.tests[content]=Test(content,testpath)
		print os.linesep
		self.statistics.write(open(self.statisticspath,'wb+'))

	def check_namelist(self):
		try:
			namelistfile=open(self.namelistpath,'rb')
		except IOError:
			print '�༶������ʧ��!���ڰ༶Ŀ¼�����\"NameList.txt\"'
			return 0
		if not namelistfile.read():
			self.set_namelist()
			return 0
		else:
			return 1

	def match_sub(self):
		#��������Ϊ���set_namelist����,����ƥ����������һ������
		maxsubs=[]
		for testname in self.tests:
			try:
				docs=str(os.listdir(self.tests[testname].path))
			except:
				print 'û�����Ŀ¼!'
			subs=self.pat.findall(docs)
			if len(maxsubs)<len(subs):
				maxsubs=subs
		return maxsubs

	def set_namelist(self):
		print '������δ����',self.classname,'������~'
		num=input('�����뱾������,���򽫳����Զ��������:')
		while not type(num) ==type(1):
			print '������������!������һ������'
			num=input()
		maxsubs=self.match_sub()
		maxsubsnum=len(maxsubs)
		if maxsubsnum>num:
			print 'Ŀǰ�����ҵ�ύ�������������ѧ������,����������������ݴ��������ļ����ļ��д�,���������'
			exit(1)
		elif maxsubsnum==num:
			print 'Ŀǰ�����ҵ�ύ�������������ѧ������,�����������������'
			namelistfile=open(self.namelistpath,'wb+')
			for sub in sorted(maxsubs):
				namelistfile.writelines(sub+os.linesep)
			namelistfile.close()
			namelistfile.close()
		else:
			print 'Ŀǰ�����ҵ�ύ��С���������ѧ������,������ӵ������᲻����,�벹���������ٿ�ʼ������������!'
			namelistfile=open(self.namelistpath,'wb+')
			for sub in sorted(maxsubs):
				namelistfile.writelines(sub+os.linesep)
			namelistfile.close()
			exit(0)

	def check_test(self,testname):
		#���������ڵ�����¼��
		self.statistics.read(self.statisticspath)
		if not self.check_namelist():
			self.set_namelist()
		namelistfile=open(self.namelistpath,'rb')
		self.stus=self.pat.findall(namelistfile.read())
		self.stunum=len(self.stus)#�༶ѧ������ֱ��ȡ��������!
		namelistfile.close()
		try:
			docs=str(os.listdir(self.tests[testname].path))
		except:
			print 'û�����Ŀ¼!'
		subs=self.pat.findall(docs)
		subnum=len(subs)
		notsub=''
		if self.statistics.has_option(testname, '�ύ����'):
			print self.classname,testname,'�Ѽ���~'
		else:
			self.statistics.set(self.tests[testname].name,'�ύ����',str(subnum)+'/'+str(self.stunum))
			print self.classname,str(subnum)+'/'+str(self.stunum), '���ύ��',self.tests[testname].name
			for stu in self.stus:
				if not stu in subs:
					notsub+=stu+','
					print stu, 'û���ύ',self.tests[testname].name
			self.statistics.set(self.tests[testname].name,'δ�ύ',notsub.rstrip(','))
		self.tests[testname].notsub=notsub.split(',')
		self.statistics.write(open(self.statisticspath,'wb+'))
		print self.classname,self.tests[testname].name,'�����ϣ����ڰ༶Ŀ¼�²鿴��¼��'+os.linesep


if __name__=='__main__':
	print '������main.py��ʼ����'
