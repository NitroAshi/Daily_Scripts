#!/usr/bin/python
#-*- coding:utf-8 -*-

import subprocess, os, time

Project_name = "As"
Project_prefix = "As"
PBS_name = "atk.pbs"
job_start = 90
job_stop = 96
job_step = 2
refresh_seconds = 5
nodes = ["node32", "node31", "node39"]


###这段其实就是"qstat | grep XXXX | wc -l"###########################
def checkflag(pjp = Project_prefix):
	checkflag1 = subprocess.Popen(["qstat"], stdout=subprocess.PIPE)
	checkflag2 = subprocess.Popen(["grep", pjp], stdin = checkflag1.stdout, stdout = subprocess.PIPE)
	checkflag3 = subprocess.Popen(["wc", "-l"], stdin = checkflag2.stdout, stdout = subprocess.PIPE)
	flag0 = int(checkflag3.communicate()[0].replace('\n',''))
	return flag0

###提交PBS任务######################################################
def qsubjob(a = 0, pjn = Project_name, node_init = 'node00'):
	dir_name = pjn + "%03d"%(a)
	os.chdir(dir_name)
	qsubjobcmd = subprocess.Popen(["qsub", PBS_name, "-l","nodes="+node_init+":ppn=16"])
	qsubjobcmd.wait()
	os.chdir("..")

###which_node_is_free#################################################
def which_node_is_free(node_name = nodes):
	tmp4 = 'node00'
	for name in node_name:
		tmp1 = subprocess.Popen(["pestat"], stdout=subprocess.PIPE)
		tmp2 = subprocess.Popen(["grep", name], stdin = tmp1.stdout, stdout = subprocess.PIPE)
		tmp3 = tmp2.communicate()
		is_free = tmp3[0].split()[1]
		is_free_check1 = len(tmp3[0].split())
		is_free_check2 = tmp3[0].split()[2][-1]
		if is_free_check1 < 10 and is_free == 'free' and is_free_check2 != '*':
			tmp4 = name
			return tmp4
	return tmp4

###主程序###########################################################
if __name__ == '__main__':
	i = job_start
	while i < job_stop+job_step:
		flag = checkflag(Project_prefix)
		if flag < len(nodes):
			node = which_node_is_free(nodes)
			qsubjob(i, Project_name, node)
			i = i + job_step
		else:
			time.sleep(refresh_seconds)




