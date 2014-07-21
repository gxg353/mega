import os,sys
d=os.path.dirname(sys.path[0])
t=os.path.basename(sys.path[0])
a=os.path.abspath(sys.path[0])
print a
os.chdir('/'.join((d,t)))
#for l in open('slow_log.py'):
#	print l
