# -*- coding: gbk -*-
import argparse
from classes import *
from handler import *
	
def main():
	parser=argparse.ArgumentParser(description='�鿴README.txt�˽����')
	#λ�ò���������һ
	parser.add_argument('command',help='ѡ����Ҫִ�е�����')
	#parse.add_argument("abc",action='store_true',default=0,help="abc")
	args=parser.parse_args()
	config=Handler()
	config.start()
	#�������ʼ�����
	if args.command=='reset':
		if config.firstuse==0:
			config.reset()
		elif config.firstuse==1:
			print '��������Ϊ�գ��������ã�'
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
		print 'ָ�����!�����Բ鿴README.txt��ð���'

if __name__=='__main__':
	main()
	
