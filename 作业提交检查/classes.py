# -*- coding: gbk -*- 
import os,re,ConfigParser
from sys import exit
#Test,Student为预留类
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
	#类方法按照依赖关系或执行顺序排序
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
		#仅在内存中添加了考试目录
		self.statistics.read(self.statisticspath)
		contents=os.listdir(self.classpath)
		for content in contents:
			testpath=os.path.join(self.classpath,content)
			if not os.path.isfile(testpath):
				if not self.statistics.has_section(content):
					self.statistics.add_section(content)
					print '新添加了',self.classname,content,'的目录'
				else:
					print self.classname,content,'已存在'
				#将所有的考试载入内存
				self.tests[content]=Test(content,testpath)
		print os.linesep
		self.statistics.write(open(self.statisticspath,'wb+'))

	def check_namelist(self):
		try:
			namelistfile=open(self.namelistpath,'rb')
		except IOError:
			print '班级名单打开失败!请在班级目录下添加\"NameList.txt\"'
			return 0
		if not namelistfile.read():
			self.set_namelist()
			return 0
		else:
			return 1

	def match_sub(self):
		#本函数仅为添加set_namelist服务,返回匹配数量最多的一个序列
		maxsubs=[]
		for testname in self.tests:
			try:
				docs=str(os.listdir(self.tests[testname].path))
			except:
				print '没有这个目录!'
			subs=self.pat.findall(docs)
			if len(maxsubs)<len(subs):
				maxsubs=subs
		return maxsubs

	def set_namelist(self):
		print '发现您未设置',self.classname,'的名单~'
		num=input('请输入本班人数,程序将尝试自动添加名单:')
		while not type(num) ==type(1):
			print '输入类型有误!请输入一个整数'
			num=input()
		maxsubs=self.match_sub()
		maxsubsnum=len(maxsubs)
		if maxsubsnum>num:
			print '目前最大作业提交数大于您输入的学生数量,可能是您输入的数据错误或测验文件夹文件有错,请检查后重试'
			exit(1)
		elif maxsubsnum==num:
			print '目前最大作业提交数等于您输入的学生数量,程序将添加完整的名单'
			namelistfile=open(self.namelistpath,'wb+')
			for sub in sorted(maxsubs):
				namelistfile.writelines(sub+os.linesep)
			namelistfile.close()
			namelistfile.close()
		else:
			print '目前最大作业提交数小于您输入的学生数量,程序添加的名单会不完整,请补充完整后再开始检测避免结果出错!'
			namelistfile=open(self.namelistpath,'wb+')
			for sub in sorted(maxsubs):
				namelistfile.writelines(sub+os.linesep)
			namelistfile.close()
			exit(0)

	def check_test(self,testname):
		#在名单存在的情况下检查
		self.statistics.read(self.statisticspath)
		if not self.check_namelist():
			self.set_namelist()
		namelistfile=open(self.namelistpath,'rb')
		self.stus=self.pat.findall(namelistfile.read())
		self.stunum=len(self.stus)#班级学生数量直接取决于名单!
		namelistfile.close()
		try:
			docs=str(os.listdir(self.tests[testname].path))
		except:
			print '没有这个目录!'
		subs=self.pat.findall(docs)
		subnum=len(subs)
		notsub=''
		if self.statistics.has_option(testname, '提交人数'):
			print self.classname,testname,'已检查过~'
		else:
			self.statistics.set(self.tests[testname].name,'提交人数',str(subnum)+'/'+str(self.stunum))
			print self.classname,str(subnum)+'/'+str(self.stunum), '人提交了',self.tests[testname].name
			for stu in self.stus:
				if not stu in subs:
					notsub+=stu+','
					print stu, '没有提交',self.tests[testname].name
			self.statistics.set(self.tests[testname].name,'未提交',notsub.rstrip(','))
		self.tests[testname].notsub=notsub.split(',')
		self.statistics.write(open(self.statisticspath,'wb+'))
		print self.classname,self.tests[testname].name,'检查完毕，可在班级目录下查看记录～'+os.linesep


if __name__=='__main__':
	print '请运行main.py开始程序！'
