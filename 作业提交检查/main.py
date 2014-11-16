# -*- coding: gbk -*-
import argparse
from classes import *
from handler import *
	
def main():
	parser=argparse.ArgumentParser(description='查看README.txt了解更多')
	#位置参数命名单一
	parser.add_argument('command',help='选择您要执行的命令')
	#parse.add_argument("abc",action='store_true',default=0,help="abc")
	args=parser.parse_args()
	config=Handler()
	config.start()
	#↑程序初始化完成
	if args.command=='reset':
		if config.firstuse==0:
			config.reset()
		elif config.firstuse==1:
			print '程序设置为空！无需重置！'
	elif args.command=='check':
		if config.firstuse==1:
			config.first_use()
		sections=config.sections()
		myclasses=[]
		for key in range(1,len(sections)):
			myclasses.append(Classes(sections[key],config.get(sections[key],'path')))
			myclasses[key-1].add_test()
		for myclass in myclasses:
			for test in myclass.tests:
				myclass.check_test(test)
	else:
		print '指令错误!您可以查看README.txt获得帮助'

if __name__=='__main__':
	main()
	
