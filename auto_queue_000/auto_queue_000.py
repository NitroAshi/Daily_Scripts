#!/usr/bin/python
#-*- coding:utf-8 -*-

import subprocess, os, time

Project_name = "As"
Project_prefix = "sif"
PBS_name = "atk.pbs"
job_start = 90
job_stop = 100
job_step = 2
refresh_seconds = 5

###这段其实就是"qstat | grep XXXX | wc -l"###########################
def checkflag(pjp = project_prefix):
	checkflag1 = subprocess.Popen(["qstat"], stdout=subprocess.PIPE)
	checkflag2 = subprocess.Popen(["grep", pjp], stdin = checkflag1.stdout, stdout = subprocess.PIPE)
	checkflag3 = subprocess.Popen(["wc", "-l"], stdin = checkflag2.stdout, stdout = subprocess.PIPE)
	flag0 = int(checkflag3.communicate()[0].replace('\n',''))
	return flag0

###提交PBS任务######################################################
def qsubjob(a = 0, pjn = Project_name):
	dir_name = pjn + "%03d"%(a)
	os.chdir(dir_name)
	qsubjobcmd = subprocess.Popen(["echo", PBS_name])
	qsubjobcmd.wait()
	os.chdir("..")

###
  

###主程序###########################################################
if __name__ == '__main__':
	i = job_start
	while i < job_stop+job_step:
		flag = checkflag(Project_prefix)
		if flag == 0:
			qsubjob(i)
			i = i + job_step
		else:
			time.sleep(refresh_seconds)




